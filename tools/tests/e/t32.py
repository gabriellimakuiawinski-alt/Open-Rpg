# Calculador de VD: caixa ao vivo no editor de inimigos, botão Usar, preenchimento automático ao salvar, fórmula contra o bestiário
from lib2 import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pm=abre_pg(b,'M','inimigos.html');pm.wait_for_timeout(2500)
    # fórmula contra as criaturas do livro (tabela livro_inimigos real)
    r=pm.evaluate("""async()=>{const x=await Mesa.db.from('livro_inimigos').select('nome,vd,dados');let n=0,h=0,h2=0;
      for(const e of x.data){if(e.nome=='Anfitrião')continue;const v=SIS.calcVD(e.dados).vd,dif=Math.abs(v-(+e.vd));n++;if(dif<=20)h++;if(dif<=40)h2++}return{n,h,h2}}""")
    chk("fórmula: 48 criaturas conferidas",r['n']==48,r)
    chk("fórmula: 70% ou mais a 1 passo do livro",r['h']/r['n']>=.7,r)
    chk("fórmula: 90% ou mais a 2 passos do livro",r['h2']/r['n']>=.9,r)
    c=pm.evaluate("[SIS.calcVD({pv:700,fort:25,refl:25,vont:15}),SIS.calcVD({}),SIS.calcVD({pv:36,vont:10}),SIS.calcVD({pv:2000,fort:35,refl:35,vont:35})]")
    chk("VD de 700 PV e testes 25/25/15 = 300",c[0]['vd']==300,c[0])
    chk("VD nunca fica abaixo de 20 e faixa é ±2 passos",c[1]['vd']==20 and c[2]['vd']>=20 and c[0]['min']==260 and c[0]['max']==340,c)
    chk("criatura enorme passa de 400",c[3]['vd']>=400,c[3])
    # editor
    pm.click('header [data-a="novo"]');pm.wait_for_timeout(500)
    chk("caixa de VD aparece no editor",pm.locator('#vdbox').count()==1 and 'VD' in pm.inner_text('#vdbox'))
    pm.fill('#e_pv','700');pm.fill('#e_fort','25');pm.fill('#e_refl','25');pm.fill('#e_vont','15');pm.wait_for_timeout(300)
    t=pm.inner_text('#vdbox')
    chk("caixa atualiza ao digitar (VD 300)",'VD 300' in t and 'entre 260 e 340' in t,t)
    chk("mostra criaturas parecidas do livro",'Parecidos do livro' in t and 'Carente' in t,t)
    pm.click('[data-vd]');chk("Usar VD preenche o campo",pm.input_value('#e_vd')=='300')
    # salvar sem VD -> preenche sozinho
    pm.fill('#e_vd','');pm.fill('#e_nome','Teste auto VD');pm.fill('#e_pv','100');pm.fill('#e_fort','10');pm.fill('#e_refl','10');pm.fill('#e_vont','5')
    pm.click('[data-s]');pm.wait_for_timeout(900)
    v=q("select to_jsonb(vd) from public.inimigos where nome='Teste auto VD'")
    chk("salvar com VD vazio calcula sozinho",str(v)=='100' or str(v) in('80','100','120'),v)
    chk("aviso de VD calculado",'calculado automaticamente' in pm.inner_text('#toast'),pm.inner_text('#toast'))
    # VD digitado à mão não é sobrescrito
    pm.click('header [data-a="novo"]');pm.wait_for_timeout(400);pm.fill('#e_nome','Teste VD manual');pm.fill('#e_vd','777');pm.fill('#e_pv','100')
    pm.click('[data-s]');pm.wait_for_timeout(900)
    chk("VD digitado é mantido",str(q("select to_jsonb(vd) from public.inimigos where nome='Teste VD manual'"))=='777')
    pm.evaluate("Mesa.db.from('inimigos').delete().in('nome',['Teste auto VD','Teste VD manual'])");pm.wait_for_timeout(500)  # não deixa sobra para o t29
    chk("sem erros",not pm.errs,pm.errs)
    b.close()
report()
