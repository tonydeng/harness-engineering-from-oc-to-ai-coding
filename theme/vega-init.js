// theme/vega-init.js
// 渲染 Vega-Lite 代码块为交互式图表，支持点击放大
document.addEventListener('DOMContentLoaded', async function() {
  const codeBlocks = document.querySelectorAll('pre code.language-vega-lite');
  if (codeBlocks.length === 0) return;

  // 动态加载 Vega-Embed（依赖已通过 book.toml additional-js 提前加载）
  if (typeof vegaEmbed === 'undefined') {
    console.error('vegaEmbed not loaded. Ensure vega.min.js, vega-lite.min.js, vega-embed.min.js are included before this script.');
    return;
  }

  const chartContainers = [];

  codeBlocks.forEach((block, index) => {
    const pre = block.parentElement;
    const container = document.createElement('div');
    container.className = 'vega-chart-container';
    container.id = 'vega-chart-' + index;

    // 用包裹 div 替换 pre
    const wrapper = document.createElement('div');
    wrapper.className = 'vega-wrapper';
    pre.parentNode.replaceChild(wrapper, pre);
    wrapper.appendChild(container);
    chartContainers.push({ container, spec: block.textContent, wrapper });
  });

  // 逐个渲染 Vega-Lite 图表
  for (const { container, spec } of chartContainers) {
    try {
      const parsed = JSON.parse(spec);
      await vegaEmbed(container, parsed, {
        actions: {
          export: true,
          source: false,
          compiled: false,
          editor: false
        },
        renderer: 'canvas',
        tooltip: true,
        theme: 'light'
      });
    } catch (err) {
      console.error('Vega-Lite rendering failed:', err);
      container.textContent = '图表渲染失败: ' + err.message;
      container.style.color = '#e74c3c';
      container.style.padding = '1em';
      container.style.border = '1px solid #e74c3c';
      container.style.borderRadius = '4px';
    }
  }
});
