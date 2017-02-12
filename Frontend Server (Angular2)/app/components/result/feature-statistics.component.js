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
var statistics_1 = require('../../models/statistic/statistics');
var FeatureStatisticsComponent = (function () {
    function FeatureStatisticsComponent() {
    }
    __decorate([
        core_1.Input(), 
        __metadata('design:type', statistics_1.Statistics)
    ], FeatureStatisticsComponent.prototype, "featureStats", void 0);
    FeatureStatisticsComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'feature-statistics',
            templateUrl: './feature-statistics.component.html',
            styleUrls: ['./feature-statistics.component.css']
        }), 
        __metadata('design:paramtypes', [])
    ], FeatureStatisticsComponent);
    return FeatureStatisticsComponent;
}());
exports.FeatureStatisticsComponent = FeatureStatisticsComponent;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=feature-statistics.component.js.map