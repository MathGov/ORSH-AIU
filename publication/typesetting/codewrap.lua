function Code(el)
 if FORMAT:match('latex') then
  if not el.text:find('[{}]') then
   return pandoc.RawInline('latex','\\nolinkurl{'..el.text..'}')
  end
 end
end
function Blocks(blocks)
 if not FORMAT:match('latex') then return nil end
 local out={};local i=1
 while i<=#blocks do
  local b=blocks[i];local nxt=blocks[i+1]
  if b.t=='Para' and #b.content==1 and b.content[1].t=='Image' and nxt and nxt.t=='Para' and pandoc.utils.stringify(nxt):match('^Figure ') then
   out[#out+1]=pandoc.RawBlock('latex','\\par\\medskip\\noindent\\begin{minipage}{\\linewidth}')
   out[#out+1]=b;out[#out+1]=nxt
   out[#out+1]=pandoc.RawBlock('latex','\\end{minipage}\\par\\medskip')
   i=i+2
  elseif b.t=='Para' and pandoc.utils.stringify(b):match('^Table ') and nxt and nxt.t=='Table' then
   out[#out+1]=pandoc.RawBlock('latex','\\Needspace{12\\baselineskip}')
   out[#out+1]=b;out[#out+1]=nxt;i=i+2
  else out[#out+1]=b;i=i+1 end
 end
 return out
end
