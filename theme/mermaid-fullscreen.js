(function () {
    const lb = document.createElement('div');
    lb.id = 'mermaid-lightbox';
    document.body.appendChild(lb);

    function bindPanZoom(svg) {
        if (svg.dataset.pzDone) return;
        svg.dataset.pzDone = '1';
        svgPanZoom(svg, {
            zoomEnabled: true,
            panEnabled: true,
            fit: true,
            center: true,
            minZoom: 0.2,
            maxZoom: 5,
            mouseWheelZoomEnabled: true
        });
    }

    // 初始 + 动态渲染
    const observer = new MutationObserver(() => {
        document.querySelectorAll('.mermaid svg').forEach(bindPanZoom);
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // 点击进入全屏
    document.addEventListener('click', e => {
        const svg = e.target.closest('.mermaid svg');
        if (!svg) return;

        const clone = svg.cloneNode(true);
        lb.innerHTML = '';
        lb.appendChild(clone);
        lb.classList.add('show');

        // 全屏里也支持 pan/zoom
        setTimeout(() => bindPanZoom(clone), 0);
    });

    // 退出全屏
    lb.addEventListener('click', () => lb.classList.remove('show'));
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') lb.classList.remove('show');
    });
})();