// theme/mermaid-init.js
document.addEventListener('DOMContentLoaded', function() {
  // 初始化 Mermaid 配置（保留之前的尺寸约束）
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    flowchart: { useMaxWidth: true, maxWidth: 100, htmlLabels: true },
    gantt: { useMaxWidth: true },
    sequenceDiagram: { useMaxWidth: true },
    classDiagram: { useMaxWidth: true },
    stateDiagram: { useMaxWidth: true },
    securityLevel: 'loose'
  });

  // 渲染 Mermaid 代码块并绑定放大功能
  const codeBlocks = document.querySelectorAll('pre code.language-mermaid');
  codeBlocks.forEach(block => {
    const pre = block.parentElement;
    const mermaidDiv = document.createElement('div');
    mermaidDiv.className = 'mermaid mermaid-container';
    mermaidDiv.textContent = block.textContent;
    pre.parentNode.replaceChild(mermaidDiv, pre);

    // 等待 Mermaid 渲染完成（异步）
    setTimeout(() => {
      const svg = mermaidDiv.querySelector('svg');
      if (svg) {
        // 1. 给 SVG 添加可点击标识，提示用户可放大
        svg.style.cursor = 'zoom-in';
        svg.dataset.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svg.outerHTML)));
        
        // 2. 包裹链接，适配 simple-lightbox
        const a = document.createElement('a');
        a.href = svg.dataset.src;
        a.className = 'mermaid-zoom-link';
        // 将 SVG 移动到链接内
        mermaidDiv.appendChild(a);
        a.appendChild(svg);
      }
    }, 500); // 等待渲染完成，可根据实际情况调整延迟
  });

  // 初始化 simple-lightbox 处理 Mermaid 放大
  if (window.simpleLightbox) {
    new SimpleLightbox({
      elements: '.mermaid-zoom-link',
      // 放大后的配置
      caption: false, // 隐藏标题
      closeText: '×', // 关闭按钮文字
      showCounter: false, // 隐藏计数器
      // 放大后 SVG 自适应弹窗
      onShow: function() {
        const img = this.currentImage.querySelector('img');
        if (img) {
          img.style.maxWidth = '90vw'; // 最大宽度 90% 视口
          img.style.maxHeight = '90vh'; // 最大高度 90% 视口
          img.style.objectFit = 'contain';
        }
      }
    });
  }
});
