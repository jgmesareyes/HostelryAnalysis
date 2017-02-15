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
var HotelsComponent = (function () {
    function HotelsComponent(hostelryService, router) {
        this.hostelryService = hostelryService;
        this.router = router;
    }
    HotelsComponent.prototype.getHotels = function () {
        var _this = this;
        this.hostelryService.getHotels()
            .then(function (results) { return _this.hotels = results; });
    };
    /*
      getMessage(): void {
        this.hostelryService
            .getMessage()
            .subscribe((data) => this.message = data.message);
      }
    */
    HotelsComponent.prototype.ngOnInit = function () {
        this.getHotels();
        //this.getMessage();
    };
    HotelsComponent.prototype.onSelect = function (hotel) {
        this.selectedHotel = hotel;
    };
    HotelsComponent.prototype.gotoDetail = function () {
        this.router.navigate(['/hotel', this.selectedHotel.name]);
    };
    HotelsComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'hotels',
            templateUrl: './hotels.component.html',
            styleUrls: ['./hotels.component.css']
        }), 
        __metadata('design:paramtypes', [hostelry_service_1.HostelryService, router_1.Router])
    ], HotelsComponent);
    return HotelsComponent;
}());
exports.HotelsComponent = HotelsComponent;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=hotels.component.js.map