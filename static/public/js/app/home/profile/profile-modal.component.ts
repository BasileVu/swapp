import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import { __platform_browser_private__,
    DomSanitizer } from '@angular/platform-browser';

import {AuthService} from "../../shared/authentication/authentication.service";
import {Subscription} from "rxjs";
import {Account} from "./account";
import {User} from "./user";
import {ToastsManager} from "ng2-toastr/ng2-toastr";
import {ItemsService} from "../items/items.service";

declare let $: any;
declare let google: any;

@Component({
    moduleId: module.id,
    selector: 'profile-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './profile-modal.component.html',
    providers: [__platform_browser_private__.BROWSER_SANITIZATION_PROVIDERS]
})

export class ProfileModalComponent implements OnInit {

    private loggedIn: boolean;
    user: User | Account;
    stars: Array<number>;
    subscription: Subscription;

    constructor(private authService : AuthService,
                private itemsService: ItemsService,
                private sanitizer: DomSanitizer,
                public toastr: ToastsManager) {}

    ngOnInit() {
        this.user = new Account();
        this.stars = [];

        this.subscription = this.authService.accountSelected$.subscribe(
            account => {
                this.showProfile(account);
            }
        );
    }

    showProfileFromUsername(username: string) {
        this.itemsService.getUser(username).then(
            user => {this.showProfile(user);},
            error => this.toastr.error(error, "Error")
        );
    }

    showProfile(account: Account | User) {

        this.user = account;
        this.fillStars(account.note_avg);
        this.sanitizer.bypassSecurityTrustUrl(this.user.profile_picture_url);

        const profileModal = $('#user-profile-modal');
        let that = this;
        profileModal.on('show.bs.modal', function (e: any) {
            setTimeout(function () {

                let pos = {
                    lat: account.coordinates.latitude,
                    lng: account.coordinates.longitude
                };

                // profile map
                const map = new google.maps.Map(document.getElementById('profile-map'), {
                    center: pos,
                    scrollwheel: false,
                    zoom: 8
                });
                const marker = new google.maps.Marker({
                    map: map,
                    position: pos
                });
                let infowindow;
                infowindow = new google.maps.InfoWindow({
                    content: '<h3 class="map-title">' +
                    account.location +
                    '</h3>'
                });
                infowindow.open(map, marker);
            }, 300)
        });
    }

    fillStars(note_avg: number) {
        let fullStars = Math.floor(note_avg);
        this.stars = Array(fullStars).fill(1);
        this.stars.push(Math.round( (note_avg % 1) * 2) / 2);
        let size = this.stars.length;
        while (5 - size++ > 0)
            this.stars.push(0);
    }
}
