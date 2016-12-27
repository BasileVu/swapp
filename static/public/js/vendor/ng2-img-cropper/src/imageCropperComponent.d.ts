import { Renderer, ElementRef, EventEmitter, AfterViewInit } from "@angular/core";
import { ImageCropper } from "./imageCropper";
import { CropperSettings } from "./cropperSettings";
export declare class ImageCropperComponent implements AfterViewInit {
    cropcanvas: ElementRef;
    settings: CropperSettings;
    image: any;
    cropper: ImageCropper;
    onCrop: EventEmitter<any>;
    croppedWidth: number;
    croppedHeight: number;
    intervalRef: number;
    renderer: Renderer;
    constructor(renderer: Renderer);
    ngAfterViewInit(): void;
    onTouchMove(event: TouchEvent): void;
    onTouchStart(event: TouchEvent): void;
    onTouchEnd(event: TouchEvent): void;
    onMouseDown(event: MouseEvent): void;
    onMouseUp(event: MouseEvent): void;
    onMouseMove(event: MouseEvent): void;
    fileChangeListener($event: any): void;
    setImage(image: HTMLImageElement): void;
    private getOrientedImage(image, callback);
}
