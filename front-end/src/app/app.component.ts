import {Component, OnInit} from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
 question = '';
  answer = '';
  isAnswer = 0;
  message = '';
  gender = '';
  age = '';
  // URL = window.location.origin + '/doc_app/';
  URL = 'http://localhost:9236/doc_app/';
  constructor(private http: HttpClient) {}
  randomExample() {
     const questions = [
      'I have ear pain since past two weeks with discharge coming out of the ear. I have also had cold for the past month. what can I do?',
       'My hair have been falling in clumps from the last 2-3 weeks. Everytime I comb or run my fingers through them many strands easily come off. I think my dandruff has increased too. Please advice me how to decrease this.',
       'I have been developing mild blisters over my lower legs, few parts in the back below neck, very few on the hands and one on the face chin. This progression I m seeing since the last 3 days with very minor additions since day 1.  What should be the right approach forward?',
       'My 22 months old son s thumb nail was swollen and had pus around thumb nail when he woke up in the morning. It s not paining as I tried touching nd checking. He was comfortable in it. Please suggest',
       'I am not able to think clearly. I have a fair job, fine relationship but something within me is making me sad and distressed. I can t focus on future. Nor can i live the present.',
       'I am having terrible ache in my lower back, at the end of my tailbone. It is concentrated at the point. I used to have this pain sometimes in the past and it used to go away in a day or two. This  time it is persisting for long and it is very intense, I can t sit properly. It won t be possible for me to visit the doctor in the next 2 or 3 days, so till then, is there anything I can do?',
       'Hi. My weight is been increasing as I have diagnosed with Hypothyroidism and I also have fatty liver with swelling in umbilical region.. Please guide me how to control my weight gain ?'
      ];
     const genders = ['M' , 'F'];
     this.question = questions[Math.floor(Math.random() * questions.length)];
     this.gender = genders[Math.floor(Math.random() * genders.length)];
     this.age = '35';
  }
  // tslint:disable-next-line:typedef
  sendRequest() {
    if ((this.question === '') || (this.gender === '') || (this.age === '')) {
      this.isAnswer = 0;
      this.message = 'Please, enter gender, age and your question.';
    } else {
      this.isAnswer = 0;
      this.message = 'Processing ....';
      const data = {inputs: ['ask_doc: g_t ' + this.gender + ' a_t ' + this.age + ' q_t ' + this.question]};
      console.log('Sending Request......');
      console.log(data);
      this.http.post(this.URL, data, {headers: {'Content-Type': 'application/json'}})
        .subscribe(
          (resp: any) => {
            console.log('Response Received');
            this.message = '';
            this.answer = resp.result;
            this.isAnswer = 1;
          },
          (error: any) => {
            console.log('Response Received with error ');
            this.message = 'Something went wrong. Please, try Again.';
            this.isAnswer = 0;
          }
        );
    }
  }

  }

