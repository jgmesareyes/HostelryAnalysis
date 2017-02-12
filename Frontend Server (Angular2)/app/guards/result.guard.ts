import { Injectable }                                                            from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot }      from '@angular/router';

import { ErrorService }      from '../services/error/error.service';


@Injectable()
export class ResultGuard implements CanActivate {

  constructor(private router: Router,
              private errorService: ErrorService) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
  	if (this.errorService.getErrorLevel() == 'ready') {
  	  return true;
  	} else {
  	  this.router.navigate(['/error']);
  	  return false;
  	}
  }

}
