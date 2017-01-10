import {OrderBy} from "./orderby";
import {Category} from "./category";
export class Search {
    public q: string;
    public category: Category;
    public orderBy: OrderBy;
    public price_min: string;
    public price_max: string;
    public range: string;

    constructor() {
        this.q = '';
        this.category = new Category("All categories");
        this.orderBy = new OrderBy("Recommended", "");
        this.price_min = '0';
        this.price_max = '0';
        this.range = '0';
    }
}