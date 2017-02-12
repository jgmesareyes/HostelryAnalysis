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
var error_service_1 = require('../services/error/error.service');
var ResultGuard = (function () {
    function ResultGuard(router, errorService) {
        this.router = router;
        this.errorService = errorService;
    }
    ResultGuard.prototype.canActivate = function (route, state) {
        if (this.errorService.getErrorLevel() == 'ready') {
            return true;
        }
        else {
            this.router.navigate(['/error']);
            return false;
        }
    };
    ResultGuard = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [router_1.Router, error_service_1.ErrorService])
    ], ResultGuard);
    return ResultGuard;
}());
exports.ResultGuard = ResultGuard;
//# sourceMappingURL=result.guard.js.map