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
var http_1 = require('@angular/http');
require('rxjs/add/operator/toPromise');
var APP_SERVER = 'http://localhost:5000/';
var IN_MEMORY_SERVER = 'api/'; //Remember de .data
var HostelryService = (function () {
    function HostelryService(http) {
        this.http = http;
        this.headers = new http_1.Headers({ 'Content-Type': 'application/json' });
    }
    HostelryService.prototype.getHotels = function () {
        var options = new http_1.RequestOptions({
            headers: this.headers
        });
        return this.http.get(APP_SERVER + 'hotels', options)
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(this.handleError);
    };
    HostelryService.prototype.getHotel = function (name) {
        var url = APP_SERVER + 'hotels/' + ("" + name);
        return this.http.get(url)
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(this.handleError);
    };
    HostelryService.prototype.getElapsedTimes = function () {
        return this.http.get(APP_SERVER + 'times')
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(this.handleError);
    };
    HostelryService.prototype.getKeywords = function () {
        return this.http.get(APP_SERVER + 'keywords')
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(this.handleError);
    };
    HostelryService.prototype.getFeatures = function () {
        return this.http.get(APP_SERVER + 'features')
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(this.handleError);
    };
    HostelryService.prototype.start = function (data) {
        var options = new http_1.RequestOptions({
            headers: this.headers,
        });
        return this.http.post(APP_SERVER + 'start', data, options)
            .toPromise()
            .then(function (response) { return response.json().success; })
            .catch(this.handleError);
    };
    HostelryService.prototype.handleError = function (error) {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    };
    HostelryService = __decorate([
        //Remember de .data
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], HostelryService);
    return HostelryService;
}());
exports.HostelryService = HostelryService;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=hostelry.service.js.map