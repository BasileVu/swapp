import {
    Component, ViewEncapsulation, OnInit
} from '@angular/core';

import { AuthService } from './../../shared/authentication/authentication.service';

@Component({
    moduleId: module.id,
    selector: 'inventory',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './inventory.component.html'
})
export class InventoryComponent implements OnInit {

    constructor(private authService: AuthService) { }

    ngOnInit(): void {
        if (this.authService.checkCredentials()) {
            console.log("credentials OK");
        } else {
            console.log("No credentials");
        }
    }
}
