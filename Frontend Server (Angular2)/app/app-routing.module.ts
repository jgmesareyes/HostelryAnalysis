import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }         from './components/dashboard/dashboard.component';
import { HotelsComponent }            from './components/hotel/hotels.component';
import { HotelDetailComponent }       from './components/hotel/hotel-detail.component';
import { ElapsedTimesComponent }      from './components/elapsed-times/elapsed-times.component';
import { ResultsComponent }           from './components/result/results.component';
import { ErrorComponent }             from './components/error/error.component';
import { ResultGuard }                from './guards/result.guard';


const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard',        component: DashboardComponent },
  { path: 'hotels',           component: HotelsComponent,            canActivate: [ResultGuard] },
  { path: 'hotel/:name',      component: HotelDetailComponent,       canActivate: [ResultGuard] },
  { path: 'times',            component: ElapsedTimesComponent,      canActivate: [ResultGuard] },
  { path: 'nlp',              component: ResultsComponent,           canActivate: [ResultGuard] },
  { path: 'error',            component: ErrorComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/