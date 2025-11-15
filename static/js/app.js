document.addEventListener('DOMContentLoaded', () => {
  const modeSelect = document.querySelector('select[name="mode"]');
  const messageRow = document.getElementById('messageRow');
  const outnameRow = document.getElementById('outnameRow');
  if (modeSelect && messageRow && outnameRow) {
    const toggle = () => {
      const isEncode = modeSelect.value === 'encode';
      messageRow.style.display = isEncode ? '' : 'none';
      outnameRow.style.display = isEncode ? '' : 'none';
    };
    modeSelect.addEventListener('change', toggle);
    toggle();
  }
});
