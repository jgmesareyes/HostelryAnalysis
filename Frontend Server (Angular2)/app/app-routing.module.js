"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var router_1 = require('@angular/router');
var setup_component_1 = require('./components/setup/setup.component');
var hotels_component_1 = require('./components/hotel/hotels.component');
var hotel_detail_component_1 = require('./components/hotel/hotel-detail.component');
var elapsed_times_component_1 = require('./components/elapsed-times/elapsed-times.component');
var results_component_1 = require('./components/result/results.component');
var error_component_1 = require('./components/error/error.component');
var result_guard_1 = require('./guards/result.guard');
var routes = [
    { path: '', redirectTo: '/setup', pathMatch: 'full' },
    { path: 'setup', component: setup_component_1.SetupComponent },
    { path: 'hotels', component: hotels_component_1.HotelsComponent, canActivate: [result_guard_1.ResultGuard] },
    { path: 'hotel/:name', component: hotel_detail_component_1.HotelDetailComponent, canActivate: [result_guard_1.ResultGuard] },
    { path: 'times', component: elapsed_times_component_1.ElapsedTimesComponent, canActivate: [result_guard_1.ResultGuard] },
    { path: 'nlp', component: results_component_1.ResultsComponent, canActivate: [result_guard_1.ResultGuard] },
    { path: 'error', component: error_component_1.ErrorComponent }
];
var AppRoutingModule = (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule = __decorate([
        core_1.NgModule({
            imports: [router_1.RouterModule.forRoot(routes)],
            exports: [router_1.RouterModule]
        }), 
        __metadata('design:paramtypes', [])
    ], AppRoutingModule);
    return AppRoutingModule;
}());
exports.AppRoutingModule = AppRoutingModule;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=app-routing.module.js.map