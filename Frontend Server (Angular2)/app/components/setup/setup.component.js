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
var error_service_1 = require('../../services/error/error.service');
var OPTIONS = {
    islands: [
        { name: 'All islands', key: 'CI' },
        { name: 'Tenerife', key: 'TF' },
        { name: 'La Palma', key: 'LP' },
        { name: 'La Gomera', key: 'LG' },
        { name: 'El Hierro', key: 'EH' },
        { name: 'Gran Canaria', key: 'GC' },
        { name: 'Fuerteventura', key: 'FV' },
        { name: 'Lanzarote', key: 'LZ' }
    ],
    languages: [
        { name: 'Spanish', key: 'SP' },
        { name: 'English', key: 'EN' }
    ],
    mode: [
        { name: 'Merge with persisting DB data', key: 'MERGE' },
        { name: 'Fetch only execution results', key: 'FETCH' }
    ]
};
var SetupComponent = (function () {
    function SetupComponent(hostelryService, errorService, router) {
        this.hostelryService = hostelryService;
        this.errorService = errorService;
        this.router = router;
        this.hotels = [];
        this.setupOptions = OPTIONS;
        this.ready = false;
    }
    SetupComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.hostelryService.getHotels()
            .then(function (hotels) { return _this.hotels = hotels; });
    };
    SetupComponent.prototype.start = function () {
        var _this = this;
        this.errorService.setErrorLevel('loading');
        var data = JSON.stringify({
            'island': this.island,
            'language': this.language,
            'mode': this.mode,
            'limit': this.limit
        });
        this.hostelryService.start(data)
            .then(function (Success) { return (_this.ready = Success,
            _this.errorService.setErrorLevel('ready'),
            _this.router.navigate(['/hotels'])); });
    };
    SetupComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'setup',
            templateUrl: './setup.component.html',
            styleUrls: ['./setup.component.css']
        }), 
        __metadata('design:paramtypes', [hostelry_service_1.HostelryService, error_service_1.ErrorService, router_1.Router])
    ], SetupComponent);
    return SetupComponent;
}());
exports.SetupComponent = SetupComponent;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=setup.component.js.map