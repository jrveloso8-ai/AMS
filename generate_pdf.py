import os
import sys
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
            self.drawString(16 * mm, 285 * mm, "Assessment de Requisitos — Automação de Suporte AMS SAP com Agentes de IA")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(16 * mm, 282 * mm, 194 * mm, 282 * mm)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(16 * mm, 14 * mm, 194 * mm, 14 * mm)
        
        self.drawString(16 * mm, 10 * mm, "Documento Técnico e Confidencial — Levantamento de Requisitos e Processos")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(194 * mm, 10 * mm, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0F2942")     # Deep Corporate Navy
    c_secondary = colors.HexColor("#1E5AA0")   # Professional Blue
    c_text = colors.HexColor("#1E293B")        # Dark Slate
    c_muted = colors.HexColor("#475569")       # Muted Slate
    c_bg_light = colors.HexColor("#F8FAFC")    # Light Box Background
    c_border = colors.HexColor("#CBD5E1")      # Border Grey
    c_accent_green = colors.HexColor("#166534")# Green Accent

    # Typography styles
    styles.add(ParagraphStyle(
        name='DocBadge',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=c_secondary,
        textTransform='uppercase',
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=c_muted,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='ObjectiveText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    ))

    styles.add(ParagraphStyle(
        name='SecHeader',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        name='SecSubtext',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=c_muted,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='FieldTitle',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_text,
        spaceBefore=4,
        spaceAfter=2
    ))

    styles.add(ParagraphStyle(
        name='BodyItem',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text
    ))

    styles.add(ParagraphStyle(
        name='TableHead',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=c_primary
    ))

    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text
    ))

    styles.add(ParagraphStyle(
        name='TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_primary
    ))

    story = []

    # Title & Badge
    story.append(Paragraph("QUESTIONÁRIO DE DESCOBERTA & LEVANTAMENTO DE REQUISITOS", styles['DocBadge']))
    story.append(Paragraph("Automação do Suporte AMS SAP com Agentes Inteligentes de IA", styles['DocTitle']))
    story.append(Paragraph("Mapeamento de Processos, Conectividade, Segurança, Governança e Infraestrutura de Modelos", styles['DocSubtitle']))

    # Objective Box
    obj_html = (
        "<b>Objetivo deste documento:</b> Mapear detalhadamente os fluxos operacionais, requisitos de integração, "
        "políticas de segurança da informação (InfoSec) e governança para a concepção e implementação de uma "
        "<b>arquitetura de Agentes Especialistas de Inteligência Artificial</b> dedicados ao suporte e manutenção de aplicações SAP "
        "(AMS Níveis 1, 2 e auxílio ao N3). A solução opera com o princípio do menor privilégio e supervisão humana assistida (Human-in-the-Loop)."
    )
    obj_table = Table([[Paragraph(obj_html, styles['ObjectiveText'])]], colWidths=[178 * mm])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('LINEBEFORE', (0,0), (0,0), 3, c_secondary),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 4 * mm))

    # SEÇÃO 1
    story.append(Paragraph("1. Escopo Funcional, Volumetria e Processo Operacional de AMS", styles['SecHeader']))
    story.append(Paragraph("Mapeia os módulos em escopo e o perfil operacional de chamados da organização.", styles['SecSubtext']))

    p1_1 = Paragraph("<b>1.1 Módulos SAP no escopo inicial do projeto:</b><br/>"
                     "[ &nbsp; ] FI (Finanças) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] CO (Controladoria) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] MM (Compras / Estoque) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] SD (Vendas / Faturamento)<br/>"
                     "[ &nbsp; ] PP (Produção) &nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] PM (Manutenção) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] QM (Qualidade) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] HR / HCM (Recursos Humanos)<br/>"
                     "[ &nbsp; ] BASIS (Sistema) &nbsp;&nbsp;&nbsp; [ &nbsp; ] ABAP (Customizados) &nbsp;&nbsp; [ &nbsp; ] Outros: __________________________________________________",
                     styles['BodyItem'])

    p1_2 = Paragraph("<b>1.2 Níveis de Atuação dos Agentes de IA no Fluxo de Atendimento:</b><br/>"
                     "<b>[ &nbsp; ] Nível 1 (Triagem & Atendimento Básico):</b> Interpretação da solicitação do usuário, categorização automática no ITSM, validação de evidências mínimas obrigatórias e esclarecimento de dúvidas frequentes de processos de negócio.<br/>"
                     "<b>[ &nbsp; ] Nível 2 (Diagnóstico Técnico & Resoluções Conhecidas):</b> Coleta automatizada de logs e evidências no SAP (Dumps, jobs cancelados, filas travadas, IDocs em erro) e execução de procedimentos operacionais padrão (SOPs).<br/>"
                     "<b>[ &nbsp; ] Nível 3 (Apoio a ABAP & Casos Complexos):</b> Pré-análise de código customizado (Z/Y), isolamento da linha exata da falha e busca cruzada de Notas Oficiais da SAP (SAP OSS Notes).",
                     styles['BodyItem'])

    p1_3 = Paragraph("<b>1.3 Volumetria e Métricas Operacionais:</b><br/>"
                     "&bull; Volume médio mensal de chamados SAP: _________________ &nbsp;&nbsp;&nbsp;&nbsp; "
                     "&bull; Backlog estimado atual: _________________<br/>"
                     "&bull; SLA Contratual: Primeira Resposta: ____________________ &nbsp;&nbsp;&nbsp;&nbsp; "
                     "&bull; Tempo Médio de Resolução: ____________________<br/>"
                     "&bull; Principais 5 a 10 tipos de incidentes mais frequentes hoje (ex.: IDoc 51, erro de faturamento, job cancelado, falta de autorização SU53, bloqueio de usuário):<br/>"
                     "____________________________________________________________________________________________________<br/>"
                     "____________________________________________________________________________________________________",
                     styles['BodyItem'])

    t_sec1 = Table([[p1_1], [p1_2], [p1_3]], colWidths=[178 * mm])
    t_sec1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec1)
    story.append(Spacer(1, 4 * mm))

    # SEÇÃO 2
    story.append(Paragraph("2. Base de Conhecimento, Histórico de Chamados e Procedimentos (RAG)", styles['SecHeader']))
    story.append(Paragraph("Insumos de conhecimento para aprendizado contextual dos agentes na metodologia da empresa.", styles['SecSubtext']))

    p2_content = Paragraph(
        "<b>2.1 Histórico de Chamados Resolvidos:</b><br/>"
        "[ &nbsp; ] Extração dos últimos 6 a 12 meses disponível &nbsp;&nbsp;&nbsp;&nbsp; "
        "Formato: [ &nbsp; ] CSV / Excel &nbsp;&nbsp; [ &nbsp; ] JSON / Banco &nbsp;&nbsp; [ &nbsp; ] Via API do ITSM<br/>"
        "<i>Campos fundamentais: Descrição do Usuário, Categoria/Módulo, Causa Raiz Identificada e Solução Técnica Aplicada.</i><br/><br/>"
        "<b>2.2 Procedimentos Operacionais Padrão (SOPs / Runbooks) e Documentações Z:</b><br/>"
        "[ &nbsp; ] Existem manuais/tutoriais de resolução para erros conhecidos da operação.<br/>"
        "[ &nbsp; ] Existe documentação técnica e funcional dos programas e tabelas customizadas (Z/Y).<br/>"
        "Onde estão armazenados atualmente? (Ex.: Confluence, SharePoint, Wiki interna, SolMan): _________________________________",
        styles['BodyItem']
    )
    t_sec2 = Table([[p2_content]], colWidths=[178 * mm])
    t_sec2.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec2)

    # BREAK TO PAGE 2
    story.append(PageBreak())

    # SEÇÃO 3
    story.append(Paragraph("3. Plataforma de Gestão de Chamados (ITSM)", styles['SecHeader']))
    story.append(Paragraph("Mapeamento das APIs para captura, atualização e interação com os chamados de suporte.", styles['SecSubtext']))

    p3_left = Paragraph("<b>3.1 Ferramenta de ITSM em Uso:</b><br/>"
                        "[ &nbsp; ] ServiceNow<br/>"
                        "[ &nbsp; ] Jira Service Management<br/>"
                        "[ &nbsp; ] SAP Solution Manager (SolMan)<br/>"
                        "[ &nbsp; ] BMC Helix / Remedy<br/>"
                        "[ &nbsp; ] Outra: ________________________", styles['BodyItem'])

    p3_right = Paragraph("<b>3.2 Capacidades de Integração via API REST:</b><br/>"
                         "[ &nbsp; ] API REST habilitada para leitura e escrita<br/>"
                         "[ &nbsp; ] Suporte a Webhooks (notificação em tempo real)<br/>"
                         "[ &nbsp; ] Permite inclusão de comentários internos (work notes)<br/>"
                         "[ &nbsp; ] Permite envio de resposta direta ao usuário<br/>"
                         "[ &nbsp; ] Permite download de prints e logs anexados", styles['BodyItem'])

    t_sec3 = Table([[p3_left, p3_right]], colWidths=[89 * mm, 89 * mm])
    t_sec3.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec3)
    story.append(Spacer(1, 4 * mm))

    # SEÇÃO 4
    story.append(Paragraph("4. Conectividade e Arquitetura do Ambiente SAP", styles['SecHeader']))
    story.append(Paragraph("Parâmetros de comunicação segura entre a camada de agentes e o ambiente SAP.", styles['SecSubtext']))

    p4_1 = Paragraph("<b>4.1 Versão do SAP e Ambientes Disponíveis:</b><br/>"
                     "Versão: [ &nbsp; ] SAP ECC 6.0 (EHP: ___) &nbsp;&nbsp; [ &nbsp; ] S/4HANA On-Premise (Ver: ___) &nbsp;&nbsp; [ &nbsp; ] S/4HANA Cloud (RISE)<br/>"
                     "Banco de Dados: [ &nbsp; ] SAP HANA &nbsp;&nbsp; [ &nbsp; ] Oracle &nbsp;&nbsp; [ &nbsp; ] MS SQL Server &nbsp;&nbsp; [ &nbsp; ] Outro: ___________<br/>"
                     "Ambientes liberados para o projeto: "
                     "[ &nbsp; ] Sandbox (SBX) &nbsp;&nbsp; [ &nbsp; ] DEV &nbsp;&nbsp; [ &nbsp; ] QAS/UAT (Validação) &nbsp;&nbsp; [ &nbsp; ] PRD (Somente Leitura)",
                     styles['BodyItem'])

    p4_2 = Paragraph("<b>4.2 Protocolos de Integração e Infraestrutura de Rede Corporativa:</b><br/>"
                     "Protocolos: [ &nbsp; ] SAP RFC / BAPI Direta (NetWeaver RFC SDK) &nbsp;&nbsp; [ &nbsp; ] SAP Gateway OData / REST &nbsp;&nbsp; [ &nbsp; ] SAP BTP / Cloud Connector<br/>"
                     "Requisitos de Rede: [ &nbsp; ] VPN Site-to-Site &nbsp;&nbsp; [ &nbsp; ] Whitelist de IPs no Firewall &nbsp;&nbsp; [ &nbsp; ] Direct Connect / ExpressRoute &nbsp;&nbsp; [ &nbsp; ] Proxy Corporativo",
                     styles['BodyItem'])

    t_sec4 = Table([[p4_1], [p4_2]], colWidths=[178 * mm])
    t_sec4.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec4)
    story.append(Spacer(1, 4 * mm))

    # SEÇÃO 5
    story.append(Paragraph("5. Segurança, Usuário Técnico e Perfis no SAP (PFCG)", styles['SecHeader']))
    story.append(Paragraph("Princípio do menor privilégio: concessão estrita de permissões de leitura (Display) para diagnóstico.", styles['SecSubtext']))

    table_data = [
        [Paragraph("Transação / Objeto", styles['TableHead']),
         Paragraph("Finalidade Operacional no Atendimento", styles['TableHead']),
         Paragraph("Status de Aprovação", styles['TableHead'])],
        [Paragraph("<b>SU53</b>", styles['TableCellBold']),
         Paragraph("Diagnóstico de falhas de autorização de usuários que abriram chamado", styles['TableCell']),
         Paragraph("[ &nbsp; ] Aprovado &nbsp; [ &nbsp; ] Em análise", styles['TableCell'])],
        [Paragraph("<b>ST22</b>", styles['TableCellBold']),
         Paragraph("Leitura de Dumps ABAP em tempo real gerados na ocorrência do erro", styles['TableCell']),
         Paragraph("[ &nbsp; ] Aprovado &nbsp; [ &nbsp; ] Em análise", styles['TableCell'])],
        [Paragraph("<b>SM21</b>", styles['TableCellBold']),
         Paragraph("Análise do System Log do SAP no intervalo de tempo do incidente", styles['TableCell']),
         Paragraph("[ &nbsp; ] Aprovado &nbsp; [ &nbsp; ] Em análise", styles['TableCell'])],
        [Paragraph("<b>SM37</b>", styles['TableCellBold']),
         Paragraph("Consulta de status e logs de execução de Jobs em background abortados", styles['TableCell']),
         Paragraph("[ &nbsp; ] Aprovado &nbsp; [ &nbsp; ] Em análise", styles['TableCell'])],
        [Paragraph("<b>WE02 / WE05</b>", styles['TableCellBold']),
         Paragraph("Monitoramento de status, dados de controle e registros de IDocs", styles['TableCell']),
         Paragraph("[ &nbsp; ] Aprovado &nbsp; [ &nbsp; ] Em análise", styles['TableCell'])],
        [Paragraph("<b>SM58 / SMQ1 / SMQ2</b>", styles['TableCellBold']),
         Paragraph("Monitoramento de filas de integração RFC síncronas/assíncronas bloqueadas", styles['TableCell']),
         Paragraph("[ &nbsp; ] Aprovado &nbsp; [ &nbsp; ] Em análise", styles['TableCell'])],
        [Paragraph("<b>Tabelas de Negócio</b>", styles['TableCellBold']),
         Paragraph("Acesso de visualização a tabelas específicas do escopo (ex.: BKPF, EKKO, VBAK)", styles['TableCell']),
         Paragraph("[ &nbsp; ] Aprovado &nbsp; [ &nbsp; ] Em análise", styles['TableCell'])],
    ]

    t_sec5 = Table(table_data, colWidths=[42 * mm, 96 * mm, 40 * mm])
    t_sec5.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sec5)

    p5_note = Paragraph("<b>Tipo de Usuário SAP:</b> Recomenda-se a criação de usuário técnico tipo <b>System (B)</b> ou <b>Communication (C)</b> sem permissão de login interativo (SAP GUI), garantindo total auditoria e controle de acesso.", styles['TableCell'])
    t_note = Table([[p5_note]], colWidths=[178 * mm])
    t_note.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#BBF7D0")),
        ('LINEBEFORE', (0,0), (0,0), 3, c_accent_green),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(t_note)

    # BREAK TO PAGE 3
    story.append(PageBreak())

    # SEÇÃO 6
    story.append(Paragraph("6. Governança de IA, Segurança da Informação (InfoSec) e LGPD", styles['SecHeader']))
    story.append(Paragraph("Garantia de conformidade corporativa, privacidade de dados e soberania da infraestrutura.", styles['SecSubtext']))

    p6_content = Paragraph(
        "<b>6.1 Provedores de Modelos de Linguagem (LLM) Homologados pela Empresa:</b><br/>"
        "[ &nbsp; ] <b>Azure OpenAI Service:</b> Instância privada executada sob a assinatura e tenant corporativo da própria empresa.<br/>"
        "[ &nbsp; ] <b>AWS Bedrock:</b> Instância privada sob a conta AWS corporativa da empresa (Claude, Llama, Titan).<br/>"
        "[ &nbsp; ] <b>Google Cloud Vertex AI:</b> Instância privada no ambiente GCP corporativo (Gemini).<br/>"
        "[ &nbsp; ] <b>Modelos Locais / On-Premise:</b> Execução interna em servidores dedicados com isolamento total de internet.<br/>"
        "[ &nbsp; ] <b>APIs Comerciais Diretas:</b> Contratos corporativos diretos OpenAI Enterprise / Anthropic.<br/><br/>"
        "<b>6.2 Políticas de Privacidade de Dados (LGPD / GDPR) e Diretrizes de Sigilo:</b><br/>"
        "[ &nbsp; ] Há necessidade de camada de mascaramento de dados (Data Masking) para PII de RH ou dados bancários/fiscais sensíveis.<br/>"
        "[ &nbsp; ] Exigência de termo de não retenção de dados para treinamento de modelos públicos (nativo nas opções privadas de nuvem).",
        styles['BodyItem']
    )
    t_sec6 = Table([[p6_content]], colWidths=[178 * mm])
    t_sec6.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec6)
    story.append(Spacer(1, 4 * mm))

    # SEÇÃO 7
    story.append(Paragraph("7. Matriz de Autonomia e Supervisão Humana (Human-in-the-Loop)", styles['SecHeader']))
    story.append(Paragraph("Evolução progressiva da autonomia operacional com controle e segurança.", styles['SecSubtext']))

    p7_1 = Paragraph("<b>[ &nbsp; ] Fase 1 — Modo Copilot / Diagnóstico Assistido (Recomendado para início):</b><br/>"
                     "Os agentes de IA executam toda a triagem no ITSM, consultam os logs e transações técnicas no SAP, cruzam com a base de conhecimento e <b>geram uma nota técnica interna no ticket com o diagnóstico exato e a solução recomendada</b>. Um analista humano do AMS revisa a recomendação antes de aplicar qualquer alteração ou responder ao usuário.", styles['BodyItem'])

    p7_2 = Paragraph("<b>[ &nbsp; ] Fase 2 — Resoluções Padronizadas com Aprovação por Clique:</b><br/>"
                     "Para incidentes de catálogo fechado e baixo risco (ex.: reprocessamento de IDoc travado por lock passageiro, reexecução de job pontual abortado), o agente prepara a ação e aguarda apenas o clique de confirmação do operador humano no ITSM.", styles['BodyItem'])

    p7_3 = Paragraph("<b>[ &nbsp; ] Fase 3 — Resolução Autônoma para Incidentes Operacionais Pré-Aprovados:</b><br/>"
                     "Resolução e encerramento automatizado com registro integral de logs de auditoria no histórico do chamado.", styles['BodyItem'])

    t_sec7 = Table([[p7_1], [p7_2], [p7_3]], colWidths=[178 * mm])
    t_sec7.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec7)
    story.append(Spacer(1, 4 * mm))

    # SEÇÃO 8
    story.append(Paragraph("8. Matriz de Stakeholders e Pontos Focais do Projeto", styles['SecHeader']))
    story.append(Paragraph("Contatos dos responsáveis técnicos e de negócio para alinhamentos e liberações.", styles['SecSubtext']))

    stakeholders_data = [
        [Paragraph("Área / Responsabilidade", styles['TableHead']),
         Paragraph("Nome do Responsável", styles['TableHead']),
         Paragraph("E-mail / Telefone", styles['TableHead'])],
        [Paragraph("<b>Líder de AMS / Operações SAP</b><br/><font color='#64748B' size=6.5>Validação funcional e aprovação de fluxos</font>", styles['TableCell']),
         Paragraph("", styles['TableCell']), Paragraph("", styles['TableCell'])],
        [Paragraph("<b>Administrador SAP BASIS</b><br/><font color='#64748B' size=6.5>Criação de usuário técnico e conectividade</font>", styles['TableCell']),
         Paragraph("", styles['TableCell']), Paragraph("", styles['TableCell'])],
        [Paragraph("<b>Segurança SAP / PFCG</b><br/><font color='#64748B' size=6.5>Concessão de perfis e autorizações mínimas</font>", styles['TableCell']),
         Paragraph("", styles['TableCell']), Paragraph("", styles['TableCell'])],
        [Paragraph("<b>Administrador da Ferramenta de ITSM</b><br/><font color='#64748B' size=6.5>Chaves de API do ServiceNow/Jira/SolMan</font>", styles['TableCell']),
         Paragraph("", styles['TableCell']), Paragraph("", styles['TableCell'])],
        [Paragraph("<b>Segurança da Informação (InfoSec / CISO)</b><br/><font color='#64748B' size=6.5>Homologação de modelos de IA, rede e LGPD</font>", styles['TableCell']),
         Paragraph("", styles['TableCell']), Paragraph("", styles['TableCell'])],
    ]

    t_sec8 = Table(stakeholders_data, colWidths=[65 * mm, 56 * mm, 57 * mm])
    t_sec8.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sec8)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF_OK")

if __name__ == "__main__":
    out_file = r"c:\Projetos Antigravity\AMS\Assessment_Requisitos_AMS_SAP_IA.pdf"
    build_pdf(out_file)
