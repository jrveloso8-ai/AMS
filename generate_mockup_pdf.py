import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(16 * mm, 285 * mm, "Arquitetura e Mockup Operacional — Agentes de IA para Suporte AMS SAP")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(16 * mm, 282 * mm, 194 * mm, 282 * mm)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(16 * mm, 14 * mm, 194 * mm, 14 * mm)
        
        self.drawString(16 * mm, 10 * mm, "Documento Conceitual & Mockup Técnico — Automação Inteligente de AMS SAP")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(194 * mm, 10 * mm, page_str)
        self.restoreState()

def build_mockup_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()
    
    # Palette
    c_primary = colors.HexColor("#0F2942")     # Deep Corporate Navy
    c_secondary = colors.HexColor("#1E5AA0")   # Professional Blue
    c_accent = colors.HexColor("#2563EB")      # Accent Blue
    c_text = colors.HexColor("#1E293B")        # Slate Dark
    c_muted = colors.HexColor("#475569")       # Slate Muted
    c_bg_light = colors.HexColor("#F8FAFC")    # Box Light
    c_border = colors.HexColor("#CBD5E1")      # Border Grey
    c_green_dark = colors.HexColor("#166534")  # Green Dark
    c_green_bg = colors.HexColor("#F0FDF4")    # Green Light
    c_dark_box = colors.HexColor("#0F172A")    # Terminal Navy

    # Styles
    styles.add(ParagraphStyle(
        name='MDocBadge',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=c_secondary,
        textTransform='uppercase',
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='MDocTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='MDocSubtitle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=c_muted,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='MSecHeader',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        name='MSecSubtext',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=c_muted,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='MBody',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text
    ))

    styles.add(ParagraphStyle(
        name='MBodySmall',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_muted
    ))

    styles.add(ParagraphStyle(
        name='MTableHead',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=c_primary
    ))

    styles.add(ParagraphStyle(
        name='MTableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text
    ))

    styles.add(ParagraphStyle(
        name='MTableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_primary
    ))

    styles.add(ParagraphStyle(
        name='MLogText',
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#F8FAFC")
    ))

    story = []

    # Title & Badge
    story.append(Paragraph("ARQUITETURA & MOCKUP CONCEITUAL DA SOLUÇÃO", styles['MDocBadge']))
    story.append(Paragraph("Operação de Suporte AMS SAP com Agentes Inteligentes de IA", styles['MDocTitle']))
    story.append(Paragraph("Desenho do Processo, Especificação dos Agentes e Simulação Real de Atendimento", styles['MDocSubtitle']))

    # Intro Card
    intro_html = (
        "<b>Visão Geral da Solução:</b> Este documento apresenta a arquitetura operacional da esteira de "
        "<b>Agentes Especialistas de Inteligência Artificial</b> aplicada ao ecossistema de suporte e manutenção SAP (AMS). "
        "O modelo atua de forma orquestrada e colaborativa: captura chamados no ITSM em tempo real, executa inspeções técnicas "
        "de telemetria no SAP (somente leitura), pesquisa bases de conhecimento históricas (RAG) e elabora diagnósticos imediatos "
        "com supervisão humana contínua (Human-in-the-Loop)."
    )
    t_intro = Table([[Paragraph(intro_html, styles['MBody'])]], colWidths=[178 * mm])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('LINEBEFORE', (0,0), (0,0), 3, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 4 * mm))

    # SEÇÃO 1: DESENHO DO PROCESSO (WORKFLOW)
    story.append(Paragraph("1. Desenho do Processo de Atendimento Ponta a Ponta", styles['MSecHeader']))
    story.append(Paragraph("Fluxo sequencial e colaborativo entre a recepção do chamado no ITSM e o diagnóstico validado no SAP.", styles['MSecSubtext']))

    # Tabela com as 5 etapas do processo
    step_data = [
        [
            Paragraph("<b>Etapa 1</b><br/><font color='#1E5AA0' size=7><b>Agente Triagem</b></font><br/><br/><b>Captura & Triagem</b><br/>Lê o ticket no ITSM em tempo real, faz OCR de prints, valida evidências e classifica módulo e severidade.", styles['MTableCell']),
            Paragraph("<b>Etapa 2</b><br/><font color='#1E5AA0' size=7><b>Agente Diagnóstico</b></font><br/><br/><b>Inspeção SAP</b><br/>Acessa o SAP via RFC/OData em modo leitura: checa Dumps (ST22), Jobs (SM37), IDocs (WE02) e SU53.", styles['MTableCell']),
            Paragraph("<b>Etapa 3</b><br/><font color='#1E5AA0' size=7><b>Agente RAG</b></font><br/><br/><b>Busca de Conhecimento</b><br/>Cruza logs com base vetorial de chamados anteriores, SOPs homologados e Notas Oficiais SAP.", styles['MTableCell']),
            Paragraph("<b>Etapa 4</b><br/><font color='#1E5AA0' size=7><b>Agente Governança</b></font><br/><br/><b>Laudo Técnico</b><br/>Sintetiza causa raiz, impacto e o roteiro exato de solução em nota interna estruturada no ticket.", styles['MTableCell']),
            Paragraph("<b>Etapa 5</b><br/><font color='#166534' size=7><b>Analista Humano</b></font><br/><br/><b>Validação 1-Clique</b><br/>Consultor confere o laudo técnico (Human-in-the-Loop) e aprova a resposta ou reprocessamento.", styles['MTableCell'])
        ]
    ]

    t_steps = Table(step_data, colWidths=[35.6 * mm] * 5)
    t_steps.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (3,0), c_bg_light),
        ('BACKGROUND', (4,0), (4,0), c_green_bg),
        ('LINEBEFORE', (4,0), (4,0), 1.5, c_green_dark),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 4 * mm))

    # Ganhos operacionais em cards compactos
    kpi_data = [
        [
            Paragraph("<b>TEMPO DE 1ª RESPOSTA</b><br/><font size=11 color='#1E5AA0'><b>&lt; 30 segundos</b></font><br/>Redução imediata em relação à média humana (30-60 min)", styles['MTableCell']),
            Paragraph("<b>TEMPO DE DIAGNÓSTICO</b><br/><font size=11 color='#166534'><b>Redução de até 85%</b></font><br/>Analista já recebe o caso com Dumps, IDoc e histórico pré-analisados", styles['MTableCell']),
            Paragraph("<b>AUDITORIA & SEGURANÇA</b><br/><font size=11 color='#0F2942'><b>100% Rastreado</b></font><br/>Conexão via usuário técnico restrito de leitura e logs no chamado", styles['MTableCell'])
        ]
    ]
    t_kpis = Table(kpi_data, colWidths=[59.3 * mm] * 3)
    t_kpis.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_kpis)

    # BREAK TO PAGE 2
    story.append(PageBreak())

    # SEÇÃO 2: EQUIPE DE AGENTES
    story.append(Paragraph("2. Equipe Digital de Agentes Especialistas de IA", styles['MSecHeader']))
    story.append(Paragraph("Especificação detalhada de responsabilidades, ferramentas e entregas de cada agente.", styles['MSecSubtext']))

    agents_table_data = [
        [
            Paragraph("Agente de IA", styles['MTableHead']),
            Paragraph("Papel & Nível de Atuação", styles['MTableHead']),
            Paragraph("Ferramentas de Integração", styles['MTableHead']),
            Paragraph("Entregável na Operação", styles['MTableHead'])
        ],
        [
            Paragraph("<b>1. Agente de Triagem & ITSM</b>", styles['MTableCellBold']),
            Paragraph("<b>Nível 1</b><br/>Recepção instantânea, interpretação de texto livre do usuário, OCR de imagens anexadas e categorização de fila.", styles['MTableCell']),
            Paragraph("&bull; API ServiceNow/Jira<br/>&bull; OCR Image Reader<br/>&bull; Ticket Classifier<br/>&bull; SLA Watchdog", styles['MTableCell']),
            Paragraph("Módulo SAP classificado, severidade ajustada e parâmetros extraídos (Ordem, Remessa, Transação).", styles['MTableCell'])
        ],
        [
            Paragraph("<b>2. Agente de Diagnóstico Técnico SAP</b>", styles['MTableCellBold']),
            Paragraph("<b>Nível 2</b><br/>Conecta ao SAP via credencial de serviço restrita (leitura) para inspecionar logs técnicos gerados no momento da falha.", styles['MTableCell']),
            Paragraph("&bull; ST22 Dump Reader<br/>&bull; SM37 Job Inspector<br/>&bull; WE02 IDoc Tracer<br/>&bull; SU53 Auth Checker<br/>&bull; SM21 SysLog Scanner", styles['MTableCell']),
            Paragraph("Dossiê técnico com o Dump exato, número de Job abortado, status do IDoc e mensagem de erro do SAP.", styles['MTableCell'])
        ],
        [
            Paragraph("<b>3. Agente de Base de Conhecimento (RAG)</b>", styles['MTableCellBold']),
            Paragraph("<b>Nível 2 / 3</b><br/>Busca semântica no histórico de chamados da organização, cruzando sintomas com resoluções conhecidas e Runbooks.", styles['MTableCell']),
            Paragraph("&bull; Vector DB Histórico<br/>&bull; Catálogo SOPs/Runbooks<br/>&bull; SAP Notes Finder<br/>&bull; Custom Z/Y Catalog", styles['MTableCell']),
            Paragraph("Procedimento Operacional Padrão (SOP) recomendado com índice de similaridade histórica.", styles['MTableCell'])
        ],
        [
            Paragraph("<b>4. Agente de Resolução & Automação</b>", styles['MTableCellBold']),
            Paragraph("<b>Nível 2</b><br/>Prepara e, quando homologado, executa procedimentos padronizados de baixo risco para incidentes rotineiros.", styles['MTableCell']),
            Paragraph("&bull; BD87 Reprocessor<br/>&bull; SM37 Job Restarter<br/>&bull; SMQ1 Unlocker<br/>&bull; SU01 User Unlocker", styles['MTableCell']),
            Paragraph("Execução segura com log de auditoria ou preparação do payload de correção para aprovação.", styles['MTableCell'])
        ],
        [
            Paragraph("<b>5. Agente de Governança & Qualidade</b>", styles['MTableCellBold']),
            Paragraph("<b>Auditoria & Conformidade</b><br/>Garante conformidade com LGPD/InfoSec, formata o laudo final e aciona o especialista humano para decisão.", styles['MTableCell']),
            Paragraph("&bull; LGPD/PII Masker<br/>&bull; Report Synthesizer<br/>&bull; Human Approval Trigger<br/>&bull; Audit Logger", styles['MTableCell']),
            Paragraph("Nota técnica interna no chamado com botão de aprovação e resposta pronta para o usuário final.", styles['MTableCell'])
        ],
    ]

    t_agents = Table(agents_table_data, colWidths=[38 * mm, 50 * mm, 45 * mm, 45 * mm])
    t_agents.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_agents)
    story.append(Spacer(1, 3 * mm))

    # Info Sec Banner
    infosec_note = Paragraph(
        "<b>Segurança e Governança Garantidas:</b> O ecossistema de agentes opera exclusivamente com "
        "<b>usuário técnico do tipo Comunicação (C) no SAP</b>, sem acesso ao SAP GUI e restrito a autorizações de visualização (Display). "
        "Nenhum dado trafegado é utilizado para treinamento de modelos públicos.",
        styles['MTableCell']
    )
    t_infonote = Table([[infosec_note]], colWidths=[178 * mm])
    t_infonote.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#BBF7D0")),
        ('LINEBEFORE', (0,0), (0,0), 3, c_green_dark),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_infonote)

    # BREAK TO PAGE 3
    story.append(PageBreak())

    # SEÇÃO 3: MOCKUP INTERATIVO DO ATENDIMENTO DE UM CHAMADO REAL
    story.append(Paragraph("3. Simulação Real de Atendimento (Mockup do Chamado no ITSM)", styles['MSecHeader']))
    story.append(Paragraph("Demonstração prática de como a inteligência dos agentes atua no atendimento de um incidente real.", styles['MSecSubtext']))

    # Ticket Header Card
    ticket_hdr = Paragraph(
        "<b>CHAMADO: INC0094821</b> &nbsp;|&nbsp; <b>Fila:</b> AMS SAP SD/FI &nbsp;|&nbsp; <b>Prioridade:</b> Alta &nbsp;|&nbsp; <b>Ambiente:</b> PRD<br/>"
        "<b>Título:</b> Falha ao liberar Nota Fiscal Eletrônica (NF-e) — Erro de Faturamento na Ordem 45009182<br/>"
        "<font color='#475569'><i>\"Ao tentar emitir a fatura via VF01 para a remessa 80019283, o sistema retornou erro e a NF-e não foi enviada para a SEFAZ. Caminhão parado na doca aguardando liberação.\" — Solicitante: Mariana Silva (Expedição)</i></font>",
        styles['MTableCell']
    )
    t_ticket_hdr = Table([[ticket_hdr]], colWidths=[178 * mm])
    t_ticket_hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('LINEBEFORE', (0,0), (0,0), 3, colors.HexColor("#DC2626")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_ticket_hdr)
    story.append(Spacer(1, 3 * mm))

    # Timeline dos Agentes
    step1_txt = Paragraph(
        "<b>[10:14:02 - +2s] Agente de Triagem & ITSM:</b><br/>"
        "Chamado capturado e OCR executado no print da usuária. Parâmetros extraídos: Ordem <b>45009182</b>, Remessa <b>80019283</b> e código de erro <b>IDoc Status 51</b>. Ticket direcionado imediatamente para a fila de diagnóstico.",
        styles['MTableCell']
    )

    log_sap = (
        "[SAP_WE02_TRACE] Conexao estabelecida com sucesso em PRD (Instancia 00).<br/>"
        "[IDOC_QUERY] IDoc localizado: #00000009841209 | Tipo: J1B_INVOICE | Status: 51 (Erro aplicacao)<br/>"
        "[ERROR_LOG] Mensagem SAP: Tabela de determinacao de contas CUST_ACC bloqueada por BATCH_JOB_FISCAL.<br/>"
        "[ST22_CHECK] Nenhum dump ABAP gerado. Lock passageiro de concorrencia detectado."
    )

    step2_txt = Paragraph(
        "<b>[10:14:09 - +9s] Agente de Diagnóstico Técnico SAP:</b><br/>"
        "Acesso de leitura realizado no SAP PRD via RFC. Consulta efetuada na transação WE02:",
        styles['MTableCell']
    )

    step3_txt = Paragraph(
        "<b>[10:14:14 - +14s] Agente de Base de Conhecimento (RAG):</b><br/>"
        "Busca semântica concluída no histórico corporativo. O erro possui <b>98.4% de similaridade</b> com o incidente <b>INC0078120</b> e com o procedimento operacional homologado <b>SOP-SD-042 (Reprocessamento de IDoc com Lock)</b>.<br/>"
        "<i>Diagnóstico Confirmado: O job fiscal encerrou às 10:13 e o objeto de lock em BSEG já está livre. O IDoc está 100% elegível para reprocessamento imediato via BD87.</i>",
        styles['MTableCell']
    )

    step4_txt = Paragraph(
        "<b>[10:14:18 - +18s] Agente de Governança & Qualidade (Human-in-the-Loop):</b><br/>"
        "Laudo técnico compilado e anexado como nota confidencial no chamado. Como a política de governança da empresa exige validação humana (Fase 1 - Copilot), a ação de reprocessamento aguarda a confirmação do consultor de plantão.",
        styles['MTableCell']
    )

    action_box = Paragraph(
        "<b>AÇÃO PRONTA PARA EXECUÇÃO: Reprocessar IDoc #00000009841209 via BD87</b><br/>"
        "Impacto: Liberação imediata da NF-e na SEFAZ e notificação automática à usuária Mariana Silva.<br/>"
        "<b>[ BOTAO DE APROVAÇÃO HUMANA: APROVAR E EXECUTAR NO SAP COM 1-CLIQUE ]</b>",
        styles['MTableCell']
    )

    t_timeline = Table([
        [step1_txt],
        [step2_txt],
        [Table([[Paragraph(log_sap, styles['MLogText'])]], colWidths=[172 * mm])],
        [step3_txt],
        [step4_txt],
        [Table([[action_box]], colWidths=[172 * mm])]
    ], colWidths=[178 * mm])

    t_timeline.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,2), (0,2), c_dark_box),
        ('BACKGROUND', (0,5), (0,5), c_green_bg),
        ('LINEBEFORE', (0,5), (0,5), 2.5, c_green_dark),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_timeline)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("MOCKUP_PDF_OK")

if __name__ == "__main__":
    out_file = r"c:\Projetos Antigravity\AMS\Mockup_Arquitetura_Processo_AMS_SAP_IA.pdf"
    build_mockup_pdf(out_file)
