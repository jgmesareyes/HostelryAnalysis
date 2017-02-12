import { Injectable }    from '@angular/core';
import { Headers, Http, RequestOptions } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Hotel }             from '../../models/hotel/hotel';
import { ElapsedTimes }      from '../../models/elapsed-times/elapsed-times';
import { Statistics }        from '../../models/statistic/statistics';


const APP_SERVER = 'http://localhost:5000/';
const IN_MEMORY_SERVER = 'api/';  //Remember de .data

@Injectable()
export class HostelryService {

  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getHotels(): Promise<Hotel[]> {
    let options: RequestOptions = new RequestOptions({
      headers: this.headers
    });
    return this.http.get(APP_SERVER + 'hotels', options)
               .toPromise()
               .then(response => response.json() as Hotel[])
               .catch(this.handleError);
  }

  getHotel(name: string): Promise<Hotel> {
    const url = APP_SERVER + 'hotels/' + `${name}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Hotel)
      .catch(this.handleError);
  }

  getElapsedTimes(): Promise<ElapsedTimes> {
    return this.http.get(APP_SERVER + 'times')
      .toPromise()
      .then(response => response.json() as ElapsedTimes)
      .catch(this.handleError);
  }

  getKeywords(): Promise<Statistics[]> {
    return this.http.get(APP_SERVER + 'keywords')
      .toPromise()
      .then(response => response.json() as Statistics[])
      .catch(this.handleError);
  }

  getFeatures(): Promise<Statistics[]> {
    return this.http.get(APP_SERVER + 'features')
      .toPromise()
      .then(response => response.json() as Statistics[])
      .catch(this.handleError);
  }

  start(data: any): Promise<boolean> {
    let options: RequestOptions = new RequestOptions({
      headers: this.headers,
    });
    return this.http.post(APP_SERVER + 'start', data, options)
        .toPromise()
        .then(response => response.json().success as boolean)
        .catch(this.handleError)
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/