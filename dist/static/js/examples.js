// All source fields are inserted as text; synthetic tool traces are never executed.
const exampleData = JSON.parse(document.getElementById('example-data').textContent);
const domainTabs = [...document.querySelectorAll('[data-example]')];
const tierButtons = [...document.querySelectorAll('[data-tier]')];
let selectedExample = 0;
let selectedTier = 'story';
const descriptions = {
  seed: 'Seed: the structured privacy context. Compare the recipient and transmission principle.',
  story: 'Story: the original narrative, including both the task benefit and sensitive context.',
  trace: 'Trace: the user’s request and simulated tool history. The model must complete the final action; no evaluated model output is shown here.'
};
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function appendFields(parent, fields) {
  const list = element('dl', undefined, 'seed-fields');
  Object.entries(fields).forEach(([key,value]) => {
    list.append(element('dt', key.replaceAll('_',' ')),element('dd',typeof value === 'string' ? value : JSON.stringify(value)));
  });
  parent.append(list);
}
function renderRecord(record, kind, explanation) {
  const article = element('article', undefined, 'example-record '+kind);
  article.append(element('h4',kind === 'appropriate' ? 'Image sharing appropriate' : 'Image sharing inappropriate','record-heading'));
  article.append(element('p',explanation,'record-explanation'));
  const body = element('div', undefined, 'record-body');
  if(selectedTier === 'seed') {
    appendFields(body,record.seed);
  } else if(selectedTier === 'story') {
    const story = element('div', undefined, 'story-text');
    record.story.content.split(/\n+/).filter(Boolean).forEach(line => story.append(element('p',line.trim())));
    body.append(story);
  } else {
    body.append(element('h5','User instruction'),element('p',record.trace.user_instruction,'user-instruction'));
    body.append(element('h5','Available toolkits'),element('p',record.trace.toolkits.join(' · ')));
    body.append(element('h5','Final action to evaluate'),element('code',record.trace.final_action));
    const detail=element('details',undefined,'trace-details');
    detail.append(element('summary','Read the original tool history'));
    const pre=element('pre');pre.append(element('code',record.trace.executable_trajectory));detail.append(pre);body.append(detail);
  }
  article.append(body,element('p','Record: '+record.id,'record-id'));
  return article;
}
function renderExample() {
  const current = exampleData.examples[selectedExample];
  domainTabs.forEach((tab,i) => {tab.setAttribute('aria-selected',String(i === selectedExample));tab.tabIndex=i===selectedExample?0:-1;});
  document.getElementById('example-panel').setAttribute('aria-labelledby',domainTabs[selectedExample].id);
  document.getElementById('example-title').textContent=current.title;
  document.getElementById('context-change').textContent=current.editorial.summary;
  const visualDescription=current.appropriate.seed.data_type;
  document.getElementById('image-metadata').textContent='Shared visual source: '+visualDescription+' · VISPR '+current.id;
  document.getElementById('example-lesson').textContent=current.editorial.changedContext;
  document.getElementById('tier-explanation').textContent=descriptions[selectedTier];
  tierButtons.forEach(button=>{const active=button.dataset.tier===selectedTier;button.setAttribute('aria-pressed',String(active));button.classList.toggle('is-dark',active);});
  document.getElementById('example-pair').replaceChildren(renderRecord(current.appropriate,'appropriate',current.editorial.appropriateExplanation),renderRecord(current.inappropriate,'inappropriate',current.editorial.inappropriateExplanation));
}
domainTabs.forEach((tab,i)=>{
  tab.addEventListener('click',()=>{selectedExample=i;renderExample();});
  tab.addEventListener('keydown',event=>{
    let next;
    if(event.key==='ArrowRight')next=(i+1)%domainTabs.length;
    if(event.key==='ArrowLeft')next=(i+domainTabs.length-1)%domainTabs.length;
    if(event.key==='Home')next=0;
    if(event.key==='End')next=domainTabs.length-1;
    if(next!==undefined){event.preventDefault();selectedExample=next;renderExample();domainTabs[next].focus();}
  });
});
tierButtons.forEach(button=>button.addEventListener('click',()=>{selectedTier=button.dataset.tier;renderExample();}));
renderExample();
