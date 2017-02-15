import { NgModule }           from '@angular/core';
import { BrowserModule }      from '@angular/platform-browser';
import { FormsModule }        from '@angular/forms';
import { HttpModule }         from '@angular/http';

import { AppRoutingModule }      from './app-routing.module';
import { AppComponent }          from './app.component';

import { SetupComponent }                  from './components/setup/setup.component';
import { HotelDetailComponent }            from './components/hotel/hotel-detail.component';
import { HotelsComponent }                 from './components/hotel/hotels.component';
import { ElapsedTimesComponent }           from './components/elapsed-times/elapsed-times.component';
import { ResultsComponent }                from './components/result/results.component';
import { KeywordStatisticsComponent}       from './components/result/keyword-statistics.component';
import { FeatureStatisticsComponent }      from './components/result/feature-statistics.component';
import { ErrorComponent }                  from './components/error/error.component';
import { HostelryService }                 from './services/hostelry/hostelry.service';
import { ErrorService }                    from './services/error/error.service';
import { ResultGuard }                     from './guards/result.guard';


@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule
  ],
  declarations: [
    AppComponent,
    SetupComponent,
    HotelDetailComponent,
    HotelsComponent,
    ElapsedTimesComponent,
    ResultsComponent,
    KeywordStatisticsComponent,
    FeatureStatisticsComponent,
    ErrorComponent
  ],
  providers: [ HostelryService, ErrorService, ResultGuard ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/