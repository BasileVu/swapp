import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {AuthService} from "../../shared/authentication/authentication.service";
import {Subscription} from "rxjs";
import {Account} from "./account";
import {User} from "./user";
import {ToastsManager} from "ng2-toastr/ng2-toastr";

declare let $: any;
declare let google: any;

@Component({
    moduleId: module.id,
    selector: 'profile-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './profile-modal.component.html'
})

export class ProfileModalComponent implements OnInit {

    private loggedIn: boolean;
    user: User | Account;
    stars: Array<number>;
    subscription: Subscription;

    constructor(private authService : AuthService,
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

    showProfile(account: Account | User) {
        this.user = account;
        this.fillStars(account.note_avg);

        const profileModal = $('#user-profile-modal');
        profileModal.on('show.bs.modal', function (e: any) {
            setTimeout(function () {

                let pos = {
                    lat: account.coordinates.latitude, // TODO
                    lng: account.coordinates.longitude // TODO
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
                if (account instanceof Account) {
                    infowindow = new google.maps.InfoWindow({
                        content: '<h3 class="map-title">' +
                        account.location.city +
                        ', ' +
                        account.location.country +
                        '</h3>'
                    });
                } else if (account instanceof User) {
                    infowindow = new google.maps.InfoWindow({
                        content: '<h3 class="map-title">' +
                        account.location +
                        '</h3>'
                    });
                } else {
                    this.toastr.error("Unknown user type", "Error");
                }
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
