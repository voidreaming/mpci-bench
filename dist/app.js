const tiers = {
  seed: ['NORMATIVE JUDGMENT', 'Who can share what with whom?', 'Structured contextual-integrity parameters describe the data subject, sender, recipient, data type, and transmission principle. Paired seeds contrast an appropriate flow with an inappropriate one.', 'Source image + structured CI parameters', 'Recognition of contextual privacy norms'],
  story: ['CONTEXTUAL REASONING', 'What changes when sharing is useful?', 'A six-sentence narrative expands the seed into a realistic social setting. Sharing the image has a concrete task benefit, requiring the model to weigh utility against the norms of the context.', 'Source image + context-rich narrative', 'Privacy–utility decisions in a social setting'],
  trace: ['AGENT ACTION', 'Will the agent act on what it knows?', 'A simulated tool-use history is truncated before the final data-transfer action. The model completes the action, allowing evaluation of leakage in inappropriate flows and useful sharing in appropriate flows.', 'User request + tools + truncated action trace', 'Actual information sharing through tool actions']
};
const tabs = [...document.querySelectorAll('[data-tier]')];
function setTier(tab) {
  tabs.forEach(t => {t.setAttribute('aria-selected', String(t === tab)); t.tabIndex = t === tab ? 0 : -1;});
  ['tier-kicker','tier-title','tier-description','tier-input','tier-test'].forEach((id,i) => document.getElementById(id).textContent = tiers[tab.dataset.tier][i]);
  document.getElementById('tier-panel').setAttribute('aria-labelledby',tab.id);
}
tabs.forEach((tab,i) => {tab.addEventListener('click',() => setTier(tab)); tab.addEventListener('keydown',e => {
  let next;
  if(e.key === 'ArrowRight') next=(i+1)%tabs.length;
  if(e.key === 'ArrowLeft') next=(i+tabs.length-1)%tabs.length;
  if(e.key === 'Home') next=0;
  if(e.key === 'End') next=tabs.length-1;
  if(next !== undefined){e.preventDefault();setTier(tabs[next]);tabs[next].focus();}
});});
const results = [['GPT-5',20.2,56.9],['GPT-4o',40.9,90.4],['Mistral-Large-3',38.7,82.1],['Gemma-3-4B',36.4,87.4],['Gemma-3-12B',36.2,88.8],['Gemma-3-27B',37.2,82.1],['InternVL3.5-8B',34.9,82.8],['InternVL3.5-14B',43.6,83.3],['Qwen3-VL-4B',30.9,79.0],['Qwen3-VL-8B',39.6,80.0],['Qwen3-VL-30B-A3B',45.2,91.6]];
function drawChart(){const family=document.getElementById('model-family').value;document.getElementById('chart').innerHTML=results.filter(r=>family==='all'||r[0].startsWith(family)).map(([name,text,visual])=>`<div class="chart-row" aria-label="${name}: text leakage ${text.toFixed(1)} percent; visual leakage ${visual.toFixed(1)} percent"><div class="model-name">${name}</div><div class="bar-pair" aria-hidden="true">${[text,visual].map((v,i)=>`<div class="bar-track" style="--value:${v}%"><div class="bar ${i?'visual':''}"></div><span class="bar-value">${v.toFixed(1)}%</span></div>`).join('')}</div></div>`).join('');}
document.getElementById('model-family').addEventListener('change',drawChart);drawChart();
document.getElementById('copy-citation').addEventListener('click',async()=>{const status=document.getElementById('copy-status');try{await navigator.clipboard.writeText(document.getElementById('bibtex').textContent);status.textContent='BibTeX copied to clipboard.';}catch{const selection=window.getSelection();const range=document.createRange();range.selectNodeContents(document.getElementById('bibtex'));selection.removeAllRanges();selection.addRange(range);status.textContent='Citation selected. Press Ctrl+C or ⌘C to copy.';}});
