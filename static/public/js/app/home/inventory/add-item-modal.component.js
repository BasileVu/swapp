"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require("@angular/core");
var forms_1 = require("@angular/forms");
var ng2_toastr_1 = require("ng2-toastr/ng2-toastr");
var inventory_service_1 = require("./inventory.service");
var item_creation_dto_1 = require("./item-creation-dto");
var key_info_1 = require("./key-info");
var DeliveryMethod = (function () {
    function DeliveryMethod(id, name) {
        this.id = id;
        this.name = name;
    }
    return DeliveryMethod;
}());
var AddItemModalComponent = (function () {
    function AddItemModalComponent(changeDetectorRef, inventoryService, formBuilder, toastr) {
        this.changeDetectorRef = changeDetectorRef;
        this.inventoryService = inventoryService;
        this.formBuilder = formBuilder;
        this.toastr = toastr;
        this.desires = new Array(1);
        this.keyInfos = new Array(1);
        this.categories = new Array();
        this.deliveryMethods = new Array();
        // images
        this.file_srcs = new Array();
        // EventEmitter to call login function of the ProfileComponent after registering
        this.newItemEvent = new core_1.EventEmitter();
        this.name = new forms_1.FormControl("", forms_1.Validators.required);
        this.min_price = new forms_1.FormControl("", forms_1.Validators.required);
        this.max_price = new forms_1.FormControl("", forms_1.Validators.required);
        this.category = new forms_1.FormControl("", forms_1.Validators.required);
        this.description = new forms_1.FormControl("", forms_1.Validators.required);
    }
    AddItemModalComponent.prototype.ngOnInit = function () {
        this.createItemForm = this.formBuilder.group({
            name: this.name,
            min_price: this.min_price,
            max_price: this.max_price,
            category: this.category,
            description: this.description
        });
        // TODO : get delivery methods
    };
    AddItemModalComponent.prototype.createItem = function () {
        var _this = this;
        var errorMessage;
        // verifications
        if (this.file_srcs.length === 0)
            errorMessage = "At least one image must be provided";
        if (this.min_price.value > this.max_price.value)
            errorMessage = "Min price must be less than max price";
        if (errorMessage != undefined) {
            this.toastr.error(errorMessage, "Error");
        }
        else {
            var deliveryM = new Array();
            var newItem_1 = new item_creation_dto_1.ItemCreationDTO("TODO", // TODO
            this.name.value, this.min_price.value, this.max_price.value, this.category.value, this.description.value, this.keyInfos, this.file_srcs, this.desires, deliveryM, new Date());
            console.log(newItem_1);
            this.inventoryService.addItem(newItem_1).then(function (res) {
                console.log(res);
                if (res.status == 201) {
                    _this.toastr.success('New item added to your inventory', 'Item created!');
                    $('#add-item-modal').modal('hide');
                    newItem_1.setUrl(res.body);
                    _this.newItemEvent.emit(newItem_1);
                }
            }, function (error) { return _this.toastr.error(error, 'Error'); });
        }
    };
    AddItemModalComponent.prototype.addDesire = function () {
        this.desires.push("");
    };
    AddItemModalComponent.prototype.removeDesire = function (index) {
        this.desires.splice(index, 1);
    };
    AddItemModalComponent.prototype.addKeyInfo = function () {
        this.keyInfos.push(new key_info_1.KeyInfo("", ""));
    };
    AddItemModalComponent.prototype.removeKeyInfo = function (index) {
        this.keyInfos.splice(index, 1);
    };
    AddItemModalComponent.prototype.removeImage = function (index) {
        this.file_srcs.splice(index, 1);
    };
    // This is called when the user selects new files from the upload button
    AddItemModalComponent.prototype.fileChange = function (input) {
        this.readFiles(input.files);
    };
    AddItemModalComponent.prototype.readFile = function (file, reader, callback) {
        // Set a callback funtion to fire after the file is fully loaded
        reader.onload = function () {
            // callback with the results
            callback(reader.result);
        };
        // Read the file
        reader.readAsDataURL(file);
    };
    AddItemModalComponent.prototype.readFiles = function (files, index) {
        var _this = this;
        if (index === void 0) { index = 0; }
        // Create the file reader
        var reader = new FileReader();
        // If there is a file
        if (index in files) {
            // Start reading this file
            this.readFile(files[index], reader, function (result) {
                // Create an img element and add the image file data to it
                var img = document.createElement("img");
                img.src = result;
                // Send this img to the resize function (and wait for callback)
                _this.resize(img, 400, 400, function (resized_jpeg, before, after) {
                    // Add the resized jpeg img source to a list for preview
                    // This is also the file you want to upload. (either as a
                    // base64 string or img.src = resized_jpeg if you prefer a file). 
                    _this.file_srcs.push(resized_jpeg);
                    // Read the next file;
                    _this.readFiles(files, index + 1);
                });
            });
        }
        else {
            // When all files are done This forces a change detection
            this.changeDetectorRef.detectChanges();
        }
    };
    AddItemModalComponent.prototype.resize = function (img, MAX_WIDTH, MAX_HEIGHT, callback) {
        var _this = this;
        // This will wait until the img is loaded before calling this function
        return img.onload = function () {
            console.log("img loaded");
            console.log(_this.file_srcs);
            // Get the images current width and height
            var width = img.width;
            var height = img.height;
            // Set the WxH to fit the Max values (but maintain proportions)
            if (width > height) {
                if (width > MAX_WIDTH) {
                    height *= MAX_WIDTH / width;
                    width = MAX_WIDTH;
                }
            }
            else {
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
            ctx.drawImage(img, 0, 0, width, height);
            // Get this encoded as a jpeg
            // IMPORTANT: 'jpeg' NOT 'jpg'
            var dataUrl = canvas.toDataURL('image/jpeg');
            // callback with the results
            callback(dataUrl, img.src.length, dataUrl.length);
        };
    };
    return AddItemModalComponent;
}());
__decorate([
    core_1.Output(),
    __metadata("design:type", Object)
], AddItemModalComponent.prototype, "newItemEvent", void 0);
AddItemModalComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'add-item-modal',
        encapsulation: core_1.ViewEncapsulation.None,
        styles: ["\n        .col-img-frame img {\n            width: 100%;\n            margin-bottom: 10px;\n        }\n        .remove-element {\n            margin-left: -6px;\n        }\n        .center {\n            text-align: center;\n        }\n    "],
        templateUrl: './add-item-modal.component.html',
        animations: [
            core_1.trigger('flyInOut', [
                core_1.state('in', core_1.style({ opacity: 1, transform: 'translateX(0)' })),
                core_1.transition('void => *', [
                    core_1.style({
                        opacity: 0,
                        transform: 'translateX(-100%)'
                    }),
                    core_1.animate('0.2s ease-in')
                ]),
                core_1.transition('* => void', [
                    core_1.animate('0.2s 10 ease-out', core_1.style({
                        opacity: 0,
                        transform: 'translateX(100%)'
                    }))
                ])
            ])
        ]
    }),
    __metadata("design:paramtypes", [core_1.ChangeDetectorRef,
        inventory_service_1.InventoryService,
        forms_1.FormBuilder,
        ng2_toastr_1.ToastsManager])
], AddItemModalComponent);
exports.AddItemModalComponent = AddItemModalComponent;
//# sourceMappingURL=add-item-modal.component.js.map