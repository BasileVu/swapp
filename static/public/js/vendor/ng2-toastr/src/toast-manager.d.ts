import { ComponentRef, ApplicationRef, ViewContainerRef, ComponentFactoryResolver } from '@angular/core';
import { ToastOptions } from './toast-options';
import { Toast } from './toast';
import { Observable } from 'rxjs/Observable';
export declare class ToastsManager {
    private componentFactoryResolver;
    private appRef;
    container: ComponentRef<any>;
    private options;
    private index;
    private toastClicked;
    private _rootViewContainerRef;
    constructor(componentFactoryResolver: ComponentFactoryResolver, appRef: ApplicationRef, options: ToastOptions);
    setRootViewContainerRef(vRef: ViewContainerRef): void;
    onClickToast(): Observable<Toast>;
    show(toast: Toast, options?: Object): Promise<Toast>;
    createTimeout(toast: Toast): any;
    setupToast(toast: Toast, options?: Object): Toast;
    private _onToastClicked(toast);
    dismissToast(toast: Toast): void;
    clearToast(toast: Toast): void;
    clearAllToasts(): void;
    dispose(): void;
    error(message: string, title?: string, options?: any): Promise<Toast>;
    info(message: string, title?: string, options?: any): Promise<Toast>;
    success(message: string, title?: string, options?: any): Promise<Toast>;
    warning(message: string, title?: string, options?: any): Promise<Toast>;
    custom(message: string, title?: string, options?: any): Promise<Toast>;
}
