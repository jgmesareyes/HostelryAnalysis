import { Component, Input }      from '@angular/core';

import { Statistics }      from '../../models/statistic/statistics';


@Component({
  moduleId: module.id,
  selector: 'feature-statistics',
  templateUrl: './feature-statistics.component.html',
  styleUrls: [ './feature-statistics.component.css' ]
})
export class FeatureStatisticsComponent {
  @Input() featureStats: Statistics;
}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/