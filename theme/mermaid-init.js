// theme/mermaid-init.js
// 用 mermaid.run() Promise 代替 setTimeout，确保 SVG 渲染完成后初始化 lightbox
document.addEventListener('DOMContentLoaded', async function() {
  // 1. 初始化 Mermaid 配置
  mermaid.initialize({
    startOnLoad: false, // 手动控制渲染
    theme: 'default',
    flowchart: { useMaxWidth: true, maxWidth: 100, htmlLabels: true },
    gantt: { useMaxWidth: true },
    sequenceDiagram: { useMaxWidth: true },
    classDiagram: { useMaxWidth: true },
    stateDiagram: { useMaxWidth: true },
    securityLevel: 'loose'
  });

  // 2. 查找所有 Mermaid 代码块，替换为 mermaid div
  const codeBlocks = document.querySelectorAll('pre code.language-mermaid');
  if (codeBlocks.length === 0) return;

  const mermaidDivs = [];
  codeBlocks.forEach(block => {
    const pre = block.parentElement;
    const mermaidDiv = document.createElement('div');
    mermaidDiv.className = 'mermaid mermaid-container';
    mermaidDiv.textContent = block.textContent;
    pre.parentNode.replaceChild(mermaidDiv, pre);
    mermaidDivs.push(mermaidDiv);
  });

  try {
    // 3. 用 mermaid.run() 异步渲染所有图表（返回 Promise，比 setTimeout 可靠）
    await mermaid.run({ nodes: mermaidDivs });

    // 4. 渲染完成后，将每个 SVG 包裹到可点击放大的 <a> 链接中
    const zoomLinks = [];
    mermaidDivs.forEach(div => {
      const svg = div.querySelector('svg');
      if (!svg) return;

      // 给 SVG 添加可点击标识
      svg.style.cursor = 'zoom-in';

      // 序列化渲染后的 SVG → base64 data URI
      const serializer = new XMLSerializer();
      const svgStr = serializer.serializeToString(svg);
      const svgData = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgStr)));

      // 创建 <a> 链接供 SimpleLightbox 使用
      const a = document.createElement('a');
      a.href = svgData;
      a.className = 'mermaid-zoom-link';
      div.appendChild(a);
      a.appendChild(svg);
      zoomLinks.push(a);
    });

    // 5. 初始化 SimpleLightbox（André Rinas 版本 v2.x）
    if (typeof SimpleLightbox !== 'undefined' && zoomLinks.length > 0) {
      // 正确 API：new SimpleLightbox(selector, options)
      const gallery = new SimpleLightbox('.mermaid-zoom-link', {
        caption: false,          // 隐藏标题
        closeText: '\u00D7',     // 关闭按钮 ×
        showCounter: false,      // 隐藏计数器
        overlayOpacity: 0.85,    // 半透明遮罩
        fileExt: false,          // 禁用扩展名检查（data URI 不匹配文件后缀）
        disableScroll: true,     // 打开时禁止页面滚动
        animationSlide: true,
        animationSpeed: 300
      });

      // 6. 用事件系统代替 onShow（v2.x 不支持 onShow 选项）
      gallery.on('show.simplelightbox', function() {
        // SimpleLightbox 将 data URI 渲染为 <img>，确保自适应视口
        const img = this.currentImage ? this.currentImage.querySelector('img') : null;
        if (img) {
          img.style.maxWidth = '90vw';
          img.style.maxHeight = '90vh';
          img.style.objectFit = 'contain';
        }
      });
    }
  } catch (err) {
    console.error('Mermaid rendering failed:', err);
  }
});
