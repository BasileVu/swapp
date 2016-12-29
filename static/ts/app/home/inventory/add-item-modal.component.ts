import {
    Component, ViewEncapsulation, OnInit, ChangeDetectorRef,
    EventEmitter, Output,
    trigger,
    state,
    style,
    transition,
    animate
} from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';

import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { InventoryService } from './inventory.service';
import { ItemCreationDTO } from './item-creation-dto';
import { KeyInfo } from './key-info';

declare let $:any;

class DeliveryMethod {
    id: number;
    name: string;
    constructor(id: number, name:string) {
        this.id = id;
        this.name = name;
    }
}

@Component({
    moduleId: module.id,
    selector: 'add-item-modal',
    encapsulation: ViewEncapsulation.None,
    styles: [`
        .col-img-frame img {
            width: 100%;
            margin-bottom: 10px;
        }
        .remove-element {
            margin-left: -6px;
        }
        .center {
            text-align: center;
        }
    `],
    templateUrl: './add-item-modal.component.html',
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
export class AddItemModalComponent implements OnInit {

    desires: Array<string> = new Array(1);
    keyInfos: Array<KeyInfo> = new Array(1);
    categories: Array<string> = new Array();
    deliveryMethods: Array<DeliveryMethod> = new Array();
    
    // images
    public file_srcs: Array<string> = new Array();

    // EventEmitter to call login function of the ProfileComponent after registering
    @Output() newItemEvent = new EventEmitter();

    // Form fields
    private createItemForm: FormGroup;
    private name = new FormControl("", Validators.required);
    private min_price = new FormControl("", Validators.required);
    private max_price = new FormControl("", Validators.required);
    private category = new FormControl("", Validators.required);
    private description = new FormControl("", Validators.required);

    constructor(private changeDetectorRef: ChangeDetectorRef,
                private inventoryService: InventoryService,
                private formBuilder: FormBuilder,
                public toastr: ToastsManager) { }

    ngOnInit(): void {
        this.createItemForm = this.formBuilder.group({
            name: this.name,
            min_price: this.min_price,
            max_price: this.max_price,
            category: this.category,
            description: this.description
        });

        // TODO : get delivery methods
    }

    createItem() {
        let errorMessage: string;
        // verifications
        if (this.file_srcs.length === 0)
            errorMessage = "At least one image must be provided";
        if (this.min_price.value > this.max_price.value)
            errorMessage = "Min price must be less than max price";

        if (errorMessage != undefined) {
            this.toastr.error(errorMessage, "Error");
        } else {
            let deliveryM = new Array<string>();

            let newItem = new ItemCreationDTO(
                "TODO", // TODO
                this.name.value,
                this.min_price.value,
                this.max_price.value,
                this.category.value,
                this.description.value,
                this.keyInfos,
                this.file_srcs,
                this.desires,
                deliveryM,
                new Date()
            );

            console.log(newItem);

            this.inventoryService.addItem(newItem).then(
                res => {
                    console.log(res);
                    if(res.status == 201) {
                        this.toastr.success('New item added to your inventory', 'Item created!');
                        $('#add-item-modal').modal('hide');
                        newItem.setUrl(res.body);
                        this.newItemEvent.emit(newItem);
                    }
                },
                error => this.toastr.error(error, 'Error')
            );
        }
        
        
    }

    addDesire() {
        this.desires.push("");
    }

    removeDesire(index) {
        this.desires.splice(index, 1);
    }

    addKeyInfo() {
        this.keyInfos.push(new KeyInfo("", ""));
    }

    removeKeyInfo(index) {
        this.keyInfos.splice(index, 1);
    }

    removeImage(index) {
        this.file_srcs.splice(index, 1);
    }
  
    // This is called when the user selects new files from the upload button
    fileChange(input){
        this.readFiles(input.files);
    }

    readFile(file, reader, callback){
        // Set a callback funtion to fire after the file is fully loaded
        reader.onload = () => {
            // callback with the results
            callback(reader.result);
        }

        // Read the file
        reader.readAsDataURL(file);
    }

    readFiles(files, index=0){
        // Create the file reader
        let reader = new FileReader();

        // If there is a file
        if (index in files) {
            // Start reading this file
            this.readFile(files[index], reader, (result) => {
                // Create an img element and add the image file data to it
                var img = document.createElement("img");
                img.src = result;
                
                // Send this img to the resize function (and wait for callback)
                this.resize(img, 400, 400, (resized_jpeg, before, after) => {

                    // Add the resized jpeg img source to a list for preview
                    // This is also the file you want to upload. (either as a
                    // base64 string or img.src = resized_jpeg if you prefer a file). 
                    this.file_srcs.push(resized_jpeg);
                    
                    // Read the next file;
                    this.readFiles(files, index+1);
                });
            });
        } else {
            // When all files are done This forces a change detection
            this.changeDetectorRef.detectChanges();
        }
    }


    resize(img, MAX_WIDTH:number, MAX_HEIGHT:number, callback) {
        // This will wait until the img is loaded before calling this function
        return img.onload = () => {
            console.log("img loaded");
            console.log(this.file_srcs);
            // Get the images current width and height
            var width = img.width;
            var height = img.height;
            
            // Set the WxH to fit the Max values (but maintain proportions)
            if (width > height) {
                if (width > MAX_WIDTH) {
                    height *= MAX_WIDTH / width;
                    width = MAX_WIDTH;
                }
            } else {
                if (height > MAX_HEIGHT) {
                    width *= MAX_HEIGHT / height;
                    height = MAX_HEIGHT;
                }
            }
            
            // create a canvas object
            var canvas = document.createElement("canvas");

            // Set the canvas to the new calculated dimensions
            canvas.width = width;
            canvas.height = height;
            var ctx = canvas.getContext("2d");  

            ctx.drawImage(img, 0, 0,  width, height); 
            
            // Get this encoded as a jpeg
            // IMPORTANT: 'jpeg' NOT 'jpg'
            var dataUrl = canvas.toDataURL('image/jpeg');
            
            // callback with the results
            callback(dataUrl, img.src.length, dataUrl.length);
        };
    }
}
