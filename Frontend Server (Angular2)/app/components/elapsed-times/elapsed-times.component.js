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
require('rxjs/add/operator/switchMap');
var core_1 = require('@angular/core');
var router_1 = require('@angular/router');
var common_1 = require('@angular/common');
var hostelry_service_1 = require('../../services/hostelry/hostelry.service');
var ElapsedTimesComponent = (function () {
    function ElapsedTimesComponent(hostelryService, route, location) {
        this.hostelryService = hostelryService;
        this.route = route;
        this.location = location;
        this.showOption = 0;
    }
    ElapsedTimesComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.route.params
            .switchMap(function (params) { return _this.hostelryService.getElapsedTimes(); })
            .subscribe(function (elapsedTimes) { return _this.elapsedTimes = elapsedTimes; });
    };
    ElapsedTimesComponent.prototype.goBack = function () {
        this.location.back();
    };
    ElapsedTimesComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'elapsed-times',
            templateUrl: './elapsed-times.component.html',
            styleUrls: ['./elapsed-times.component.css']
        }), 
        __metadata('design:paramtypes', [hostelry_service_1.HostelryService, router_1.ActivatedRoute, common_1.Location])
    ], ElapsedTimesComponent);
    return ElapsedTimesComponent;
}());
exports.ElapsedTimesComponent = ElapsedTimesComponent;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=elapsed-times.component.js.map