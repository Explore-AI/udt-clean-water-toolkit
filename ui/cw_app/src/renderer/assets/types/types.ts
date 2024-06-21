export type Assets = {
    gid: number, 
    geometry: string, 
    dmas: number[], 
    modified_at: string, 
    created_at: string, 
    geometry_4326?: string, 
}

export type Mains = {
    gid: number, 
    geometry: string, 
    dmas: number[], 
    modified_at: string, 
    created_at: string, 
    geometry_4326?: string,
    material?: string, 
    diameter?: number, 
}

type DrfPagination = {
    current_page: number, 
    first_item_index: number, 
    last_item_index: number,
    next_page: number, 
    num_items: number,
    num_pages: number,
    page_size: number,
    prev_page?: number | null,  
}

export type ApiResponse = {
    pagination?: DrfPagination, 
    items: Assets[] | Mains[], 
}

export type TableContextType = {
    <Type>(uiParams: Type): Type, 
    setTableUiParams: () => void; 
}

export type TabSelectType = {
    selectedKey: string
}