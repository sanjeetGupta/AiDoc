import t5
import functools
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import argparse
import tensorflow_datasets as tfds
from constants import TPU_NAME, MODEL_DIR,DATA_DIR,TPU_TOPOLOGY,BASE_PRETRAINED_DIR
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
tf.executing_eagerly()

### PARAMETERS ###
parser = argparse.ArgumentParser()
parser.add_argument("--version", default=None, type=str, required=True,help="Version Name")
parser.add_argument("--train_data_file", default=None, type=str, required=True,help="The input training data file (a text file).")
parser.add_argument("--eval_data_file", default=None, type=str,required=True,help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
parser.add_argument("--dev_data_file", default=None, type=str,required=True,help="An optional input validation data file to evaluate the perplexity on (a text file).")
parser.add_argument("--prefix", default=None, type=str,required=True,help="prefix to input string")
parser.add_argument("--tpu", default=None, type=str,required=True,help="tpu name")
parser.add_argument("--model_type", default="small",required=True, type=str,help="The model architecture to be fine-tuned.") #["small", "base", "large", "3B", "11B"]
parser.add_argument("--epoch", default=1, type=int, help=" number of epochs")
parser.add_argument("--batch_size", default=1, type=int, help=" batch size")
args = parser.parse_args()
print(args)

## CONSTANTS ########################################
VERSION=args.version
tf.io.gfile.makedirs(MODEL_DIR)
PREFIX=args.prefix
tsv_input_file={
                'train':[os.path.join(DATA_DIR, args.train_data_file)]*args.epoch, ##2
                'test': [os.path.join(DATA_DIR, args.eval_data_file)] , ##3
                'validation':[os.path.join(DATA_DIR, args.dev_data_file)] ##4
               }
## Count examples
num_examples={}
for key in tsv_input_file:
    num_examples[key]=0
    for file in tsv_input_file[key]:
        print(file)
        with tf.io.gfile.GFile(file, 'r') as f:
            num_examples[key]=num_examples[key]+len(f.readlines())

print('n_examples',num_examples)
## MODEL INFO
MODEL_SIZE = args.model_type  ##4
model_parallelism, train_batch_size, keep_checkpoint_max = {
    "small": (1, 256, 16),
    "base": (2, 128, 8),
    "large": (8, 64, 4),
    "3B": (8, 16, 1),
    "11B": (8, 16, 1)}[MODEL_SIZE]
train_batch_size=args.batch_size
FINETUNE_STEPS = int(num_examples['train']/train_batch_size)
print('Total {} model,{} examples, {} epochs, {} steps,{} batch size'.format(args.model_type,num_examples['train'],args.epoch,FINETUNE_STEPS,train_batch_size))
## Public GCS path for T5 pre-trained model checkpoints
PRETRAINED_DIR = os.path.join(BASE_PRETRAINED_DIR, MODEL_SIZE)





### DATASET FN
def dataset_fn(split, shuffle_files=False):
    # We only have one file for each split.
    del shuffle_files
    # Load lines from the text file as examples.
    ds = tf.data.TextLineDataset(tsv_input_file[split])
    # Split each "<input>\t<target>" example into (input, target) tuple.
    ds = ds.map(functools.partial(tf.io.decode_csv, record_defaults=["", ""],
                    field_delim="\t", use_quote_delim=False),
    num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # Map each tuple to a {"input": ... "target": ...} dict.
    ds = ds.map(lambda *ex: dict(zip(["input", "target"], ex)))
    return ds

def normalize_text(text):
    """remove quotes from a TensorFlow string."""
    text = tf.strings.regex_replace(text,"'(.*)'", r"\1")
    return text

def summarize(dataset, article_key, summary_key):
  def my_fn(x):
    """Convert to a text2text example."""
    strs_to_join = [PREFIX, x[article_key]]
    return {
        'inputs': normalize_text(tf.strings.join(strs_to_join, separator=' ')),
        'targets': normalize_text(x[summary_key]),
    }
  return dataset.map(my_fn, num_parallel_calls=tf.data.experimental.AUTOTUNE)




t5.data.TaskRegistry.add(
    "text_gen",
    dataset_fn=dataset_fn,
    splits=["train", "validation","test"],
    text_preprocessor=functools.partial(summarize, article_key="input",summary_key="target"),
    metric_fns=[t5.evaluation.metrics.rouge],
    sentencepiece_model_path=t5.data.DEFAULT_SPM_PATH)

nq_task = t5.data.TaskRegistry.get("text_gen")
ds = nq_task.get_dataset(split="train", sequence_length={"inputs": 128, "targets": 256})
print("A few preprocessed validation examples...")
for ex in tfds.as_numpy(ds.take(5)):
  print(ex)




print('DEFINING MODEL')
model = t5.models.MtfModel(
    model_dir=MODEL_DIR,
    tpu=TPU_NAME,
    tpu_topology=TPU_TOPOLOGY,
    model_parallelism=model_parallelism,
    batch_size=train_batch_size,
    sequence_length={"inputs": 128, "targets": 256},
    learning_rate_schedule=0.003,
    save_checkpoints_steps=int(FINETUNE_STEPS/args.epoch)-32,
    keep_checkpoint_max=keep_checkpoint_max,
    iterations_per_loop=32
)


print('fine-tuning model for {} steps'.format(FINETUNE_STEPS))
model.finetune(
    mixture_or_task_name="text_gen",
    pretrained_model_dir=PRETRAINED_DIR,
    finetune_steps=FINETUNE_STEPS
)
model.batch_size = train_batch_size


print('Evaluation of validation')
model.eval(
    mixture_or_task_name="text_gen",
    checkpoint_steps="all",
    split="validation"
)

print('Evaluation of test')
model.eval(
    mixture_or_task_name="text_gen",
    checkpoint_steps="all",
    split="test",
)



