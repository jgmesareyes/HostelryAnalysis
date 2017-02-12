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
var hostelry_service_1 = require('../../services/hostelry/hostelry.service');
var ResultsComponent = (function () {
    //  sectorId: number = 1;
    function ResultsComponent(hostelryService, router, route) {
        this.hostelryService = hostelryService;
        this.router = router;
        this.route = route;
        this.statisticsMode = 1;
    }
    ResultsComponent.prototype.getKeywords = function () {
        var _this = this;
        this.hostelryService
            .getKeywords()
            .then(function (statistics) { return _this.statistics = statistics; });
    };
    ResultsComponent.prototype.getFeatures = function () {
        var _this = this;
        this.hostelryService
            .getFeatures()
            .then(function (statistics) { return _this.statistics = statistics; });
    };
    ResultsComponent.prototype.ngOnInit = function () {
        this.getKeywords();
    };
    ResultsComponent.prototype.changeStatisticsMode = function () {
        if (this.statisticsMode != 1) {
            this.statisticsMode = 1;
            this.getKeywords();
        }
        else {
            this.statisticsMode = 0;
            this.getFeatures();
        }
        this.sectorStatistics = null;
    };
    ResultsComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'results',
            templateUrl: './results.component.html',
            styleUrls: ['./results.component.css']
        }), 
        __metadata('design:paramtypes', [hostelry_service_1.HostelryService, router_1.Router, router_1.ActivatedRoute])
    ], ResultsComponent);
    return ResultsComponent;
}());
exports.ResultsComponent = ResultsComponent;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=results.component.js.map