import { IHeaderParams, IInnerHeaderComponent } from 'ag-grid-community';

export interface ILinkHeaderParams {
    url?: string;
    headerName?: string;
}

export class LinkHeaderComponent implements IInnerHeaderComponent {
    private agParams!: ILinkHeaderParams & IHeaderParams;
    private eGui!: HTMLDivElement;
    private eText!: HTMLElement;
    private eLink!: HTMLAnchorElement;

    init(agParams: ILinkHeaderParams & IHeaderParams) {
        this.agParams = agParams;
        
        const eGui = (this.eGui = document.createElement('div'));
        eGui.classList.add('link-header-component');
        eGui.style.cssText = `
            display: flex;
            align-items: center;
            justify-content: flex-start;
            height: 100%;
            width: 100%;
            padding-left: 8px;
        `;

        // 创建🔗链接元素
        if (agParams.url) {
            const eLink = (this.eLink = document.createElement('a'));
            eLink.href = agParams.url;
            eLink.target = '_blank';
            eLink.rel = 'noopener noreferrer';
            eLink.innerHTML = '🔗';
            eLink.style.cssText = `
                margin-right: 4px;
                font-size: 14px;
                text-decoration: none;
                color: inherit;
                cursor: pointer;
            `;
            
            // 添加点击事件，阻止冒泡
            eLink.addEventListener('click', (e) => {
                e.stopPropagation();
            });
            
            eGui.appendChild(eLink);
        }

        // 创建文本元素
        const textNode = document.createElement('span');
        this.eText = textNode;
        textNode.textContent = agParams.headerName || agParams.displayName;
        eGui.appendChild(textNode);
    }

    getGui() {
        return this.eGui;
    }

    refresh(params: ILinkHeaderParams & IHeaderParams) {
        this.eText.textContent = params.headerName || params.displayName;
        
        // 更新链接
        if (params.url && this.eLink) {
            this.eLink.href = params.url;
        }
        
        return true;
    }
}

export default LinkHeaderComponent; 