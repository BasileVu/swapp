import { Routes, RouterModule }  from '@angular/router';

import { HomeComponent } from './home.component';

// noinspection TypeScriptValidateTypes
const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
        children: [
            //{ path: 'treeview', component: TreeViewComponent }
        ]
    }
];

export const routing = RouterModule.forChild(routes);
