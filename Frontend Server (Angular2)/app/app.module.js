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
var platform_browser_1 = require('@angular/platform-browser');
var forms_1 = require('@angular/forms');
var http_1 = require('@angular/http');
var app_routing_module_1 = require('./app-routing.module');
var app_component_1 = require('./app.component');
var setup_component_1 = require('./components/setup/setup.component');
var hotel_detail_component_1 = require('./components/hotel/hotel-detail.component');
var hotels_component_1 = require('./components/hotel/hotels.component');
var elapsed_times_component_1 = require('./components/elapsed-times/elapsed-times.component');
var results_component_1 = require('./components/result/results.component');
var keyword_statistics_component_1 = require('./components/result/keyword-statistics.component');
var feature_statistics_component_1 = require('./components/result/feature-statistics.component');
var error_component_1 = require('./components/error/error.component');
var hostelry_service_1 = require('./services/hostelry/hostelry.service');
var error_service_1 = require('./services/error/error.service');
var result_guard_1 = require('./guards/result.guard');
var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        core_1.NgModule({
            imports: [
                platform_browser_1.BrowserModule,
                forms_1.FormsModule,
                http_1.HttpModule,
                app_routing_module_1.AppRoutingModule
            ],
            declarations: [
                app_component_1.AppComponent,
                setup_component_1.SetupComponent,
                hotel_detail_component_1.HotelDetailComponent,
                hotels_component_1.HotelsComponent,
                elapsed_times_component_1.ElapsedTimesComponent,
                results_component_1.ResultsComponent,
                keyword_statistics_component_1.KeywordStatisticsComponent,
                feature_statistics_component_1.FeatureStatisticsComponent,
                error_component_1.ErrorComponent
            ],
            providers: [hostelry_service_1.HostelryService, error_service_1.ErrorService, result_guard_1.ResultGuard],
            bootstrap: [app_component_1.AppComponent]
        }), 
        __metadata('design:paramtypes', [])
    ], AppModule);
    return AppModule;
}());
exports.AppModule = AppModule;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=app.module.js.map