import { Component, OnInit }      from '@angular/core';
import { Router }                 from '@angular/router';

import { Hotel }                from '../../models/hotel/hotel';
import { SetupOptions }         from '../../models/setup-options/setup-options';
import { HostelryService }      from '../../services/hostelry/hostelry.service';
import { ErrorService }         from '../../services/error/error.service';


const OPTIONS: SetupOptions = {
  islands: [
  	{name: 'All islands', key: 'CI'},
  	{name: 'Tenerife', key: 'TF'},
  	{name: 'La Palma', key: 'LP'},
  	{name: 'La Gomera', key: 'LG'},
  	{name: 'El Hierro', key: 'EH'},
  	{name: 'Gran Canaria', key: 'GC'},
  	{name: 'Fuerteventura', key: 'FV'},
  	{name: 'Lanzarote', key: 'LZ'}
  ],
  languages: [
  	{name: 'Spanish', key: 'SP'},
  	{name: 'English', key: 'EN'}
  ],
  mode: [
  	{name: 'Merge with persisting DB data', key: 'MERGE'},
  	{name: 'Fetch only execution results', key: 'FETCH'}
  ]
};


@Component({
  moduleId: module.id,
  selector: 'my-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})

export class DashboardComponent implements OnInit {
  hotels: Hotel[] = [];
  setupOptions = OPTIONS;
  island: string;
  language: string;
  mode: string;
  limit: number;
  ready: boolean = false;
  readyLevel: string;

  constructor(private hostelryService: HostelryService,
              private errorService: ErrorService,
  	          private router: Router) { }

  ngOnInit(): void {
    this.hostelryService.getHotels()
      .then(hotels => this.hotels = hotels);
  }

  start(): void {
    this.errorService.setErrorLevel('loading');
    let data = JSON.stringify({
      'island': this.island,
      'language': this.language,
      'mode': this.mode,
      'limit': this.limit
    });
    this.hostelryService.start(data)
      .then(Success => (this.ready = Success,
                        this.errorService.setErrorLevel('ready'),
                        this.router.navigate(['/hotels'])));
  }

}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/