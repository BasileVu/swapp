import {OrderBy} from "./orderby";
export class Search {
    public q: string;
    public category: string;
    public orderBy: OrderBy;
    public price_min: string;
    public price_max: string;
    public range: string;
}