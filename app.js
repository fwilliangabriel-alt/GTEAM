'use strict';
document.documentElement.classList.add('js');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const track=document.querySelector('.gallery-track');
const cards=[...track.querySelectorAll('.media-card')];
let visible=cards;
const status=document.querySelector('.gallery-status');
const arrows=[...document.querySelectorAll('[data-direction]')];
function updateArrows(){arrows[0].disabled=track.scrollLeft<4;arrows[1].disabled=track.scrollLeft+track.clientWidth>=track.scrollWidth-4;}
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
 document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 cards.forEach(card=>{card.hidden=button.dataset.filter!=='all'&&card.dataset.type!==button.dataset.filter;const video=card.querySelector('video');if(video)pause(video);});
 visible=cards.filter(c=>!c.hidden);track.scrollTo({left:0,behavior:'instant'});
 status.textContent=`${visible.length} registros · ${button.textContent} · Deslize ou use as setas para explorar`;
 requestAnimationFrame(updateArrows);
}));
function move(direction){track.scrollBy({left:direction*(visible[0]?.getBoundingClientRect().width+20||track.clientWidth),behavior:reduced.matches?'instant':'smooth'});}
arrows.forEach(b=>b.addEventListener('click',()=>move(Number(b.dataset.direction))));
track.addEventListener('keydown',e=>{if(e.target!==track)return;if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();move(e.key==='ArrowLeft'?-1:1);}});
track.addEventListener('scroll',updateArrows,{passive:true});window.addEventListener('resize',updateArrows);updateArrows();
const lightbox=document.querySelector('.lightbox');
document.querySelectorAll('.enlarge').forEach(a=>a.addEventListener('click',e=>{
 if(typeof lightbox.showModal!=='function')return;
 e.preventDefault();const img=a.querySelector('img');lightbox.querySelector('img').src=a.href;lightbox.querySelector('img').alt=img.alt;lightbox.querySelector('p').textContent=img.alt;
 lightbox.showModal();
}));
const privacy=document.querySelector('.privacy-dialog');document.querySelector('.privacy-trigger').addEventListener('click',()=>privacy.showModal());
document.querySelectorAll('dialog').forEach(dialog=>{dialog.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});});
// Keep native controls. Autoplay only visible videos, respecting motion and data preferences.
const videos=[...document.querySelectorAll('video')];
const userPaused=new WeakSet();
videos.forEach(video=>{video.addEventListener('pause',()=>{if(!video.dataset.autoPause)userPaused.add(video);delete video.dataset.autoPause;});});
function pause(video){if(!video.paused){video.dataset.autoPause='true';video.pause();}}
if('IntersectionObserver' in window){
 const videoObserver=new IntersectionObserver(entries=>entries.forEach(({target:video,isIntersecting})=>{
  if(!isIntersecting||document.hidden||video.closest('[hidden]')){pause(video);return;}
  if(!reduced.matches&&!navigator.connection?.saveData&&!userPaused.has(video)){video.muted=true;video.play().catch(()=>{});}
 }),{threshold:.65});videos.forEach(v=>videoObserver.observe(v));
 const revealObserver=new IntersectionObserver(entries=>entries.forEach(({target,isIntersecting})=>{if(isIntersecting){target.classList.add('is-visible');revealObserver.unobserve(target);}}),{threshold:.08});
 if(!reduced.matches)document.querySelectorAll('.about-image,.about-copy,.benefit,.section-heading,.plan,.process li').forEach(el=>{el.classList.add('reveal-pending');revealObserver.observe(el);});
}
document.addEventListener('visibilitychange',()=>{if(document.hidden)videos.forEach(pause);});
reduced.addEventListener('change',()=>{if(reduced.matches)videos.forEach(pause);});
window.addEventListener('pagehide',()=>videos.forEach(pause));
