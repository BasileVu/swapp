import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {AuthService} from "../../shared/authentication/authentication.service";
import {Subscription} from "rxjs";
import {Account} from "./account";

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
    user: Account;
    stars: Array<number>;
    subscription: Subscription;

    constructor(private authService : AuthService) {}

    ngOnInit() {
        this.user = new Account();
        this.stars = [];

        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => {
                this.loggedIn = loggedIn;

                if (loggedIn) {
                    this.authService.getAccount().then(
                        account => {
                            this.user = account;
                            this.fillStars(account.note_avg);

                            console.log(account);
                            console.log(this.user);

                            const profileModal = $('#user-profile-modal');
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
                                    const infowindow = new google.maps.InfoWindow({
                                        content: '<h3 class="map-title">'+
                                            account.location.city +
                                            ', '+
                                            account.location.country +
                                            '</h3>'
                                    });
                                    infowindow.open(map, marker);
                                }, 300)
                            });
                        }
                    );
                }
            }
        );
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
