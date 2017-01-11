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
import {ProfileService} from "../profile/profile.service";
import {SearchService} from "../search/search.service";
import {Category} from "../search/category";
import {DetailedItem} from "../items/detailed-item";

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

    keyInfos: Array<KeyInfo> = [];
    categories: Array<Category> = [];
    deliveryMethods: Array<DeliveryMethod> = [];
    userDeliveryMethods: Array<number> = [];
    newItemId: number;
    
    // images
    file_srcs: Array<string> = [];
    files: Array<File> = [];
    data: any;

    // EventEmitter to inform subscribed components after an item creation
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
                private searchService: SearchService,
                private formBuilder: FormBuilder,
                public toastr: ToastsManager) { }

    ngOnInit(): void {
        // Init item creation form
        this.createItemForm = this.formBuilder.group({
            name: this.name,
            min_price: this.min_price,
            max_price: this.max_price,
            category: this.category,
            description: this.description
        });

        // Get all categories
        this.searchService.getCategories().then(
            categories => this.categories = categories,
            error => this.toastr.error("Can't get all categories", "Error")
        );

        // Get all delivery methods
        this.inventoryService.getDeliveryMethods().then(
            deliveryMethods => {
                this.deliveryMethods = deliveryMethods;
            },
            error => this.toastr.error("Can't get all delivery methods")
        );

        // Add a blank key info
        this.keyInfos.push(new KeyInfo("", ""));
    }

    // Add or remove the delivery method if selected/unselected
    updateCheckbox(deliverymethod_id: number, checked: boolean) {
        if (checked) {
            this.userDeliveryMethods.push(+deliverymethod_id);
        } else {
            let index = this.userDeliveryMethods.indexOf(+deliverymethod_id, 0);
            if (index > -1) {
                this.userDeliveryMethods.splice(index, 1);
            }
        }
    }

    // Create the item if valid
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
            // Create the item

            // Build a proper keyInfos array with trimmed values
            let keyInfos = new Array<KeyInfo>();
            for (let ki of this.keyInfos)
                if (ki.key && ki.key.trim() && ki.info && ki.info.trim())
                    keyInfos.push(new KeyInfo(ki.key.trim(), ki.info.trim()));

            let newItem = new ItemCreationDTO(
                this.name.value,
                this.min_price.value,
                this.max_price.value,
                this.category.value,
                this.description.value,
                keyInfos,
                this.userDeliveryMethods
            );

            this.inventoryService.addItem(newItem)
                .then(
                    res => {
                        // images can be added only after item creation (api constraint)
                        this.newItemId = AddItemModalComponent.getItemIdFromResponse(res);
                        this.addImages(this.newItemId);
                    },
                    error => this.toastr.error(error, 'Error'));
        }
    }

    // Get the id of newly created item
    static getItemIdFromResponse(res: any) {
        let obj: DetailedItem = JSON.parse(res._body);
        return obj.id;
    }

    // Add images to the newly created item
    addImages(item_id: number) {
        if (this.files.length > 6) {
            this.toastr.error("Cannot add more than 6 images", "Error");
        } else {
            let filesUploaded: number = 0;
            for (let f of this.files) {
                let formData:FormData = new FormData();
                formData.append('image', f, f.name);
                formData.append('item', item_id);
                this.inventoryService.addImage(formData, item_id)
                    .then( // now signal the ProfileComponent that we uploaded picture
                        res => {
                            if (++filesUploaded === this.files.length) {
                                this.toastr.success('New item added to your inventory', 'Item created!');
                                this.newItemEvent.emit(this.newItemId);
                                $('#add-item-modal').modal('hide');
                                this.resetForm();
                            }
                        },
                        error => this.toastr.error(error, "Error")
                    );
            }
        }
    }

    resetForm() {
        this.createItemForm.reset();
        this.keyInfos = [];
        this.keyInfos.push(new KeyInfo("", ""));
        this.userDeliveryMethods = [];
        this.file_srcs = [];
        this.files = [];
        this.data = {};
        // Get all delivery methods
        this.inventoryService.getDeliveryMethods().then(
            deliveryMethods => {
                this.deliveryMethods = deliveryMethods;
            },
            error => this.toastr.error("Can't get all delivery methods")
        );
    }

    addKeyInfo() {
        this.keyInfos.push(new KeyInfo("", ""));
    }

    removeKeyInfo(index: number) {
        this.keyInfos.splice(index, 1);
    }

    removeImage(index: number) {
        this.file_srcs.splice(index, 1);
        this.files.splice(index, 1);
    }
  
    // Called when the user selects new files from the upload button
    fileChange(input: any){
        for (let f of input.files)
            this.files.push(f);

        this.readFiles(input.files);
    }

    // Read one file
    readFile(file: File, reader: FileReader, callback: any){
        // Set a callback funtion to fire after the file is fully loaded
        reader.onload = () => {
            // callback with the results
            callback(reader.result);
        };

        // Read the file
        reader.readAsDataURL(file);
    }

    // Read many files
    readFiles(files: Array<File>, index=0){
        // Create the file reader
        let reader = new FileReader();

        // If there is a file
        if (index in files) {
            // Start reading this file
            this.readFile(files[index], reader, (result: string) => {
                // Create an img element and add the image file data to it
                const img = document.createElement("img");
                img.src = result;
                
                // Send this img to the resize function (and wait for callback)
                this.resize(img, 800, 500, (resized_jpeg: string, before: any, after: any) => {

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

    // Resize image to display it correctly for the user
    resize(img: any, MAX_WIDTH:number, MAX_HEIGHT:number, callback: any) {
        // This will wait until the img is loaded before calling this function
        return img.onload = () => {
            // Get the images current width and height
            let width = img.width;
            let height = img.height;
            
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
            const canvas = document.createElement("canvas");

            // Set the canvas to the new calculated dimensions
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");

            ctx.drawImage(img, 0, 0,  width, height); 
            
            // Get this encoded as a jpeg
            // IMPORTANT: 'jpeg' NOT 'jpg'
            const dataUrl = canvas.toDataURL('image/jpeg'); // TODO : png
            
            // callback with the results
            callback(dataUrl, img.src.length, dataUrl.length);
        };
    }
}
