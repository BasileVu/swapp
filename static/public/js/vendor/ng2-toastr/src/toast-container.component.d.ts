import { ChangeDetectorRef } from '@angular/core';
import { Toast } from './toast';
import { ToastOptions } from './toast-options';
import { DomSanitizer } from '@angular/platform-browser';
export declare class ToastContainer {
    private sanitizer;
    private cdr;
    position: string;
    messageClass: string;
    titleClass: string;
    positionClass: string;
    toasts: Toast[];
    maxShown: number;
    newestOnTop: boolean;
    animate: string;
    private onToastClicked;
    constructor(sanitizer: DomSanitizer, cdr: ChangeDetectorRef, options: ToastOptions);
    addToast(toast: Toast): void;
    removeToast(toast: Toast): void;
    removeAllToasts(): void;
    clicked(toast: Toast): void;
    anyToast(): boolean;
    findToast(toastId: number): Toast | void;
}
