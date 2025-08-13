import { IHeaderParams, IInnerHeaderComponent } from "ag-grid-community"

export interface ILinkHeaderParams {
  url?: string
  headerName?: string
}

export class LinkHeaderComponent implements IInnerHeaderComponent {
  private agParams!: ILinkHeaderParams & IHeaderParams
  private eGui!: HTMLDivElement
  private eText!: HTMLElement
  private eLink!: HTMLAnchorElement

  init(agParams: ILinkHeaderParams & IHeaderParams) {
    this.agParams = agParams

    const eGui = (this.eGui = document.createElement("div"))
    eGui.classList.add("link-header-component")
    eGui.style.cssText = `
            display: flex;
            align-items: center;
            justify-content: flex-start;
            height: 100%;
            width: 100%;
            box-sizing: border-box;
            overflow: hidden;
            min-width: 0;
            padding-left: 8px;
        `

    // 不启用自动换行和自动表头高度，保持单行显示

    // 创建🔗链接元素
    if (agParams.url) {
      const eLink = (this.eLink = document.createElement("a"))
      eLink.href = agParams.url
      eLink.target = "_blank"
      eLink.rel = "noopener noreferrer"
      eLink.innerHTML = "🔗"
      eLink.style.cssText = `
                margin-right: 4px;
                font-size: 14px;
                text-decoration: none;
                color: inherit;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                flex: 0 0 auto;
            `

      // 添加点击事件，阻止冒泡
      eLink.addEventListener("click", (e) => {
        e.stopPropagation()
      })

      eGui.appendChild(eLink)
    }

    // 创建文本元素
    const textNode = document.createElement("span")
    this.eText = textNode
    textNode.textContent = agParams.headerName || agParams.displayName
    textNode.style.cssText = `
            flex: 1 1 auto;
            min-width: 0;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        `
    // 悬浮提示显示完整标题
    const fullTitle = textNode.textContent || ""
    textNode.title = fullTitle
    eGui.title = fullTitle
    eGui.appendChild(textNode)

    // 延迟设置列宽，确保DOM渲染完成后再测量
    // 使用更长的延迟和重试机制确保调整成功
    setTimeout(() => {
      this.adjustColumnWidth()
    }, 100)

    // 额外的重试机制，确保宽度调整成功
    setTimeout(() => {
      this.adjustColumnWidth()
    }, 500)
  }

  private adjustColumnWidth() {
    try {
      const col = this.agParams.column as any
      const colApi = (this.agParams as any).columnApi
      const gridApi = (this.agParams as any).api

      if (!col || !colApi || !gridApi) {
        console.warn(
          "LinkHeaderComponent: Missing required APIs for width adjustment"
        )
        return
      }

      // 获取当前列的实际宽度
      const currentWidth =
        col.getActualWidth?.() || col.getColDef?.()?.width || 100

      // 测量文本实际需要的宽度
      const text = this.eText.textContent || ""
      const textWidth = this.measureTextWidth(text)

      // 计算需要的总宽度
      const paddingLeft = 8
      const iconWidth = this.agParams.url ? 20 : 0
      const iconGap = this.agParams.url ? 4 : 0
      const extra = 30 // 右侧内边距 + 排序/过滤图标空间
      const requiredWidth = Math.max(
        textWidth + paddingLeft + iconWidth + iconGap + extra,
        150 // 设置最小宽度为150px，确保文本不会过度压缩
      )

      console.log(
        `LinkHeaderComponent [${text}]: currentWidth=${currentWidth}, requiredWidth=${requiredWidth}, textWidth=${textWidth}`
      )

      // 如果当前宽度不够，则扩展列宽
      if (requiredWidth > currentWidth) {
        const newWidth = Math.ceil(requiredWidth)

        // 使用 gridApi 的 setColumnWidths 方法，更可靠
        try {
          const colId = col.getColId?.() || col.getColDef?.()?.field
          if (colId) {
            gridApi.setColumnWidths([{ key: colId, newWidth }])
            console.log(
              `LinkHeaderComponent [${text}]: Successfully set width to ${newWidth}px using gridApi.setColumnWidths`
            )
            return // 成功则退出
          }
        } catch (e) {
          console.warn(
            `LinkHeaderComponent [${text}]: gridApi.setColumnWidths failed:`,
            e
          )

          // 如果 setColumnWidths 失败，尝试 columnApi
          try {
            colApi.setColumnWidth(col, newWidth)
            console.log(
              `LinkHeaderComponent [${text}]: Successfully set width to ${newWidth}px using columnApi.setColumnWidth`
            )
            return // 成功则退出
          } catch (e2) {
            console.warn(
              `LinkHeaderComponent [${text}]: columnApi.setColumnWidth failed:`,
              e2
            )

            // 最后的回退方案：直接设置 colDef
            const colDef = col.getColDef?.()
            if (colDef) {
              colDef.width = newWidth
              // 同时设置minWidth确保宽度不会被压缩
              colDef.minWidth = Math.min(newWidth, 150)
              gridApi.refreshHeader()
              console.log(
                `LinkHeaderComponent [${text}]: Set width ${newWidth}px via colDef as fallback`
              )
            }
          }
        }
      } else {
        console.log(
          `LinkHeaderComponent [${text}]: Current width ${currentWidth}px is sufficient`
        )
      }
    } catch (error) {
      console.warn("LinkHeaderComponent: Failed to adjust column width:", error)
    }
  }

  private measureTextWidth(text: string): number {
    try {
      // 创建临时元素来测量文本宽度
      const temp = document.createElement("span")
      temp.style.cssText = `
        position: absolute;
        visibility: hidden;
        white-space: nowrap;
        font-family: inherit;
        font-size: inherit;
        font-weight: inherit;
      `
      temp.textContent = text
      document.body.appendChild(temp)

      const width = temp.offsetWidth
      document.body.removeChild(temp)

      return width
    } catch (_) {
      // 回退到 canvas 测量
      try {
        const canvas = document.createElement("canvas")
        const ctx = canvas.getContext("2d")
        if (ctx) {
          ctx.font = window.getComputedStyle(this.eText).font
          return Math.ceil(ctx.measureText(text).width)
        }
      } catch (_) {
        // 最后的回退：估算宽度
        return text.length * 8
      }
    }
    return 0
  }

  getGui() {
    return this.eGui
  }

  refresh(params: ILinkHeaderParams & IHeaderParams) {
    // 更新参数
    this.agParams = params

    // 更新链接
    if (params.url && this.eLink) {
      this.eLink.href = params.url
    }

    // 更新文本内容
    const newText = params.headerName || params.displayName
    const oldText = this.eText.textContent

    if (newText !== oldText) {
      this.eText.textContent = newText
      const fullTitle = newText || ""
      this.eText.title = fullTitle
      this.eGui.title = fullTitle

      // 重新调整列宽（多次尝试确保成功）
      setTimeout(() => {
        this.adjustColumnWidth()
      }, 100)

      setTimeout(() => {
        this.adjustColumnWidth()
      }, 500)
    }

    return true
  }
}

export default LinkHeaderComponent
