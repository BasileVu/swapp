import {
    Component, OnInit, ViewEncapsulation, style,
    animate, transition, state, trigger
} from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'update-profile-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './update-profile-modal.component.html',
    animations: [
        trigger('flyInOut', [
            state('in', style({opacity: 1, transform: 'translateX(0)'})),
            transition('void => *', [
                style({
                    opacity: 0,
                    transform: 'translateX(-100%)'
                }),
                animate('0.2s ease-in')
            ]),
            transition('* => void', [
                animate('0.2s 10 ease-out', style({
                    opacity: 0,
                    transform: 'translateX(100%)'
                }))
            ])
        ])
    ]
})

export class UpdateProfileModalComponent implements OnInit {

    desires: Array<any> = [];

    constructor() {}

    ngOnInit() {
    }

    addDesire() {
        this.desires.push("");
    }

    removeDesire(index: number) {
        this.desires.splice(index, 1);
    }
}
