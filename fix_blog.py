from bs4 import BeautifulSoup, NavigableString
from pathlib import Path
import pandas as pd
import re, json, html
from urllib.parse import urlparse
from difflib import get_close_matches

SITE='https://epitomeofhatred.com'
root=Path('/mnt/data/worksite')
blog_dir=root/'blog'

audit=pd.read_csv('/mnt/data/blog-audit.csv')
audit_map={r['file']:r for _,r in audit.iterrows()}
valid_slugs={p.stem for p in blog_dir.glob('*.html') if p.name!='index.html'}

# common source links for source blocks / plain-text source mentions
source_map=[
    ('PBS NewsHour','https://www.pbs.org/newshour/'),
    ('Washington Post','https://www.washingtonpost.com/'),
    ('New York Times','https://www.nytimes.com/'),
    ('The New York Times','https://www.nytimes.com/'),
    ('Wall Street Journal','https://www.wsj.com/'),
    ('Los Angeles Times','https://www.latimes.com/'),
    ('Associated Press','https://apnews.com/'),
    ('AP','https://apnews.com/'),
    ('Reuters','https://www.reuters.com/'),
    ('CNN','https://www.cnn.com/'),
    ('NPR','https://www.npr.org/'),
    ('Politico','https://www.politico.com/'),
    ('Axios','https://www.axios.com/'),
    ('Politifact','https://www.politifact.com/'),
    ('PolitiFact','https://www.politifact.com/'),
    ('BBC','https://www.bbc.com/news'),
    ('NBC News','https://www.nbcnews.com/'),
    ('CBS News','https://www.cbsnews.com/'),
    ('ABC News','https://abcnews.go.com/'),
    ('ProPublica','https://www.propublica.org/'),
    ('The Atlantic','https://www.theatlantic.com/'),
    ('Bloomberg','https://www.bloomberg.com/'),
    ('The Guardian','https://www.theguardian.com/us'),
    ('USA Today','https://www.usatoday.com/'),
    ('Congress.gov','https://www.congress.gov/'),

    ('State Department','https://www.state.gov/'),
    ('IAEA','https://www.iaea.org/'),
    ('National Security Council','https://www.whitehouse.gov/nsc/'),
    ('Congressional Record','https://www.congress.gov/congressional-record'),
    ('Senate records','https://www.senate.gov/'),
    ('Senate','https://www.senate.gov/'),
    ('FCC.gov','https://www.fcc.gov/'),
    ('FCC','https://www.fcc.gov/'),
    ('University of Maryland','https://www.umd.edu/'),
    ('NY AG Letitia James','https://ag.ny.gov/'),
    ('Department of Education','https://www.ed.gov/'),
    ('US District Court','https://www.uscourts.gov/'),
    ('District Court','https://www.uscourts.gov/'),
    ('AllSides','https://www.allsides.com/'),
    ('Federal News Network','https://federalnewsnetwork.com/'),
    ('Harvard Kennedy School','https://www.hks.harvard.edu/'),
    ('CBPP','https://www.cbpp.org/'),
    ('Economic Policy Institute','https://www.epi.org/'),
    ('DOL','https://www.dol.gov/'),
    ('Department of Labor','https://www.dol.gov/'),
    ('SEC','https://www.sec.gov/'),
    ('AFL-CIO','https://aflcio.org/'),
    ('National Employment Law Project','https://www.nelp.org/'),
    ('NELP','https://www.nelp.org/'),
    ('NIOSH','https://www.cdc.gov/niosh/'),
    ('Center for Public Integrity','https://publicintegrity.org/'),
    ('National Partnership for Women and Families','https://nationalpartnership.org/'),
    ('Federal Reserve','https://www.federalreserve.gov/'),
    ('Federal Reserve Act','https://www.federalreserve.gov/aboutthefed/fract.htm'),
    ('14th Amendment','https://constitution.congress.gov/browse/amendment-14/'),
    ('Wong Kim Ark','https://supreme.justia.com/cases/federal/us/169/649/'),
    ('Supreme Court','https://www.supremecourt.gov/'),
    ('Supreme Court of the United States','https://www.supremecourt.gov/'),
    ('Federal Register','https://www.federalregister.gov/'),
    ('White House','https://www.whitehouse.gov/'),
    ('DOJ','https://www.justice.gov/'),
    ('Department of Justice','https://www.justice.gov/'),
    ('DHS','https://www.dhs.gov/'),
    ('HHS','https://www.hhs.gov/'),
    ('CDC','https://www.cdc.gov/'),
    ('NIH','https://www.nih.gov/'),
    ('CMS','https://www.cms.gov/'),
    ('EPA','https://www.epa.gov/'),
    ('USDA','https://www.usda.gov/'),
    ('Treasury','https://home.treasury.gov/'),
    ('IRS','https://www.irs.gov/'),
    ('FBI','https://www.fbi.gov/'),
    ('CIA','https://www.cia.gov/'),
    ('DNI','https://www.dni.gov/'),
    ('CBO','https://www.cbo.gov/'),
    ('GAO','https://www.gao.gov/'),
    ('USCIS','https://www.uscis.gov/'),
    ('CBP','https://www.cbp.gov/'),
    ('CISA','https://www.cisa.gov/'),
    ('FEMA','https://www.fema.gov/'),
    ('OMB','https://www.whitehouse.gov/omb/'),
    ('Kaiser Family Foundation','https://www.kff.org/'),
    ('KFF','https://www.kff.org/'),
    ('American Farm Bureau Federation','https://www.fb.org/'),
    ('American Immigration Council','https://www.americanimmigrationcouncil.org/'),
    ('Center for American Progress','https://www.americanprogress.org/'),
    ('Peterson Institute for International Economics','https://www.piie.com/'),
    ('US Census Bureau','https://www.census.gov/'),
    ('Census Bureau','https://www.census.gov/'),
    ('ASCE','https://infrastructurereportcard.org/'),
    ('IEA','https://www.iea.org/'),
    ('University of Oslo','https://www.uio.no/english/'),
    ('Change.org','https://www.change.org/'),
]

# longer first to avoid AP inside unrelated words
source_map=sorted(source_map, key=lambda x: len(x[0]), reverse=True)

def trunc(s, n=158):
    s=' '.join((s or '').split())
    if len(s)<=n: return s
    cut=s[:n+1]
    if ' ' in cut: cut=cut.rsplit(' ',1)[0]
    return cut.rstrip(' .,:;') + '…'

def slug_to_title(slug):
    return slug.replace('-', ' ').title()

def maybe_fix_blog_href(href):
    if not href.startswith('/blog/'): return href, False
    slug=href[len('/blog/'):].strip('/').split('#')[0]
    if slug in valid_slugs or slug in ('', 'index'): return href, False
    # manual overrides first
    manual={
        'republicans-held-tsa-hostage-for-ice':'dhs-shutdown-ice-funding-hostage',
        'trump-called-bin-laden-in-his-book-he-did-not':'trump-book-did-not-predict-911',
        'lafayette-square-bible-photo':'lafayettte-square-bible-photo',
        'abandoning-kurds-syria':'abandon-kurds-syria',
    }
    target=manual.get(slug)
    if not target:
        parts=set(slug.split('-'))
        best=None; best_score=0
        for cand in valid_slugs:
            cparts=set(cand.split('-'))
            score=len(parts & cparts) / max(1, len(parts | cparts))
            if score>best_score:
                best_score=score; best=cand
        if best_score>=0.45:
            target=best
    if target:
        suffix=''
        if '#' in href: suffix='#'+href.split('#',1)[1]
        return '/blog/'+target+suffix, True
    return href, False

def text_to_fragments(text):
    # linkify known sources in source blocks only
    changed=False
    pieces=[text]
    for name,url in source_map:
        new=[]
        pattern=re.compile(rf'(?<![\w>])({re.escape(name)})(?![\w<])')
        for piece in pieces:
            if not isinstance(piece, str):
                new.append(piece); continue
            pos=0
            for m in pattern.finditer(piece):
                before=piece[pos:m.start()]
                if before: new.append(before)
                frag=BeautifulSoup(f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(m.group(1))}</a>', 'html.parser').a
                new.append(frag)
                pos=m.end()
                changed=True
            rest=piece[pos:]
            if rest: new.append(rest)
        pieces=new
    return pieces, changed

def linkify_source_blocks(soup):
    changed=False
    # candidate parents likely to contain citation prose
    candidates=[]
    for el in soup.select('.fact-block, .fact-source, .sources, .source-list, .receipt-list'):
        candidates.append(el)
    # also exact label+parent patterns
    for label in soup.find_all(string=re.compile(r'The Sources|Sources|Receipts|Source Trail', re.I)):
        p=label.parent
        if p and p.parent and p.parent not in candidates:
            candidates.append(p.parent)
    seen=set()
    for parent in candidates:
        if id(parent) in seen: continue
        seen.add(id(parent))
        for node in list(parent.descendants):
            if isinstance(node, NavigableString):
                if not node.strip():
                    continue
                if node.parent and node.parent.name in ('a','script','style'):
                    continue
                frags, did=text_to_fragments(str(node))
                if did:
                    changed=True
                    last=node
                    first_insert=True
                    for frag in frags:
                        if isinstance(frag, str):
                            if first_insert:
                                node.replace_with(frag)
                                last=parent.find(string=frag) if False else None
                                first_insert=False
                            else:
                                new_str=NavigableString(frag)
                                # insert after previous inserted element/string
                                if hasattr(last,'insert_after'):
                                    last.insert_after(new_str)
                                else:
                                    # fallback append to parent
                                    parent.append(new_str)
                                last=new_str
                        else:
                            if first_insert:
                                node.replace_with(frag)
                                first_insert=False
                            else:
                                if hasattr(last,'insert_after'):
                                    last.insert_after(frag)
                                else:
                                    parent.append(frag)
                            last=frag
                    if first_insert:
                        pass
    return changed

def collect_external_links(soup):
    links=[]
    seen=set()
    for a in soup.find_all('a', href=True):
        href=a['href']
        if href.startswith('http'):
            if href not in seen:
                seen.add(href)
                txt=' '.join(a.get_text(' ', strip=True).split()) or urlparse(href).netloc
                links.append((txt, href))
    return links

def ensure_head_style(soup):
    head=soup.head
    if not head: return False
    style_text='''\n  .site-note { background: var(--bg2); border: 1px solid var(--border); border-left: 3px solid var(--accent2); padding: 1.4rem 1.6rem; margin: 2.5rem 0; }\n  .site-note .label { font-family: var(--font-mono); font-size: 0.68rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent2); margin-bottom: 0.55rem; display: block; }\n  .site-note p { font-size: 0.98rem !important; line-height: 1.65; margin: 0 !important; color: var(--text-muted) !important; }\n  .site-note ul { margin: 0.7rem 0 0; padding-left: 1.1rem; }\n  .site-note li { margin: 0.35rem 0; color: var(--text-muted); }\n  .site-note a { color: var(--accent2); }\n'''
    if style_text.strip() not in str(head):
        style=soup.new_tag('style')
        style.string=style_text
        head.append(style)
        return True
    return False

def make_note(soup, label, html_inner):
    div=soup.new_tag('div', attrs={'class':'site-note'})
    span=soup.new_tag('span', attrs={'class':'label'})
    span.string=label
    div.append(span)
    frag=BeautifulSoup(html_inner, 'html.parser')
    for child in list(frag.contents):
        div.append(child)
    return div

def existing_note_labels(soup):
    return {t.get_text(' ', strip=True).lower() for t in soup.select('.site-note .label, .fact-block .label, .fact-section-header span')}


def extract_deck(soup):
    deck=soup.select_one('.deck')
    if deck:
        return ' '.join(deck.get_text(' ', strip=True).split())
    return ''

def first_body_paragraph(soup):
    p=soup.select_one('.post-body p')
    return ' '.join(p.get_text(' ', strip=True).split()) if p else ''

for path in blog_dir.glob('*.html'):
    if path.name=='index.html':
        continue
    html_text=path.read_text(encoding='utf-8')
    soup=BeautifulSoup(html_text, 'html.parser')
    changed=False
    slug=path.stem
    row=audit_map.get(path.name)
    tags_text=' '.join([x.get_text(' ', strip=True).lower() for x in soup.select('.post-tag')])
    is_personal='personal' in tags_text or slug in ('i-almost-ran-for-congress','i-said-what-i-said')

    # canonical
    head=soup.head
    if head:
        canon=head.find('link', rel='canonical')
        target=f'{SITE}/blog/{slug}'
        if canon:
            if canon.get('href')!=target:
                canon['href']=target; changed=True
        else:
            link=soup.new_tag('link', rel='canonical', href=target)
            # place after description if possible
            desc=head.find('meta', attrs={'name':'description'})
            if desc:
                desc.insert_after(link)
            else:
                head.append(link)
            changed=True

        # meta description normalize
        desc=head.find('meta', attrs={'name':'description'})
        ogdesc=head.find('meta', attrs={'property':'og:description'})
        new_desc=None
        if ogdesc and ogdesc.get('content') and 80 <= len(ogdesc['content']) <= 160:
            new_desc=' '.join(ogdesc['content'].split())
        elif desc and desc.get('content'):
            new_desc=trunc(desc['content'])
            if len(new_desc)<80:
                deck=extract_deck(soup) or first_body_paragraph(soup)
                if deck:
                    new_desc=trunc(deck)
        else:
            deck=extract_deck(soup) or first_body_paragraph(soup)
            new_desc=trunc(deck)
        if new_desc:
            if desc:
                if desc.get('content')!=new_desc:
                    desc['content']=new_desc; changed=True
            else:
                m=soup.new_tag('meta')
                m.attrs['name']='description'; m.attrs['content']=new_desc
                head.append(m); changed=True
            # sync twitter if too long or missing
            tw=head.find('meta', attrs={'name':'twitter:description'})
            if tw:
                if tw.get('content')!=new_desc:
                    tw['content']=new_desc; changed=True
            else:
                tw=soup.new_tag('meta')
                tw.attrs['name']='twitter:description'; tw.attrs['content']=new_desc
                head.append(tw); changed=True

    # fix internal blog hrefs
    for a in soup.find_all('a', href=True):
        new_href, did = maybe_fix_blog_href(a['href'])
        if did:
            a['href']=new_href; changed=True

    # ensure styles for notes exist
    if ensure_head_style(soup):
        changed=True

    # linkify source mentions inside source blocks
    if linkify_source_blocks(soup):
        changed=True

    # add source trail / context block if missing dedicated final block
    labels=existing_note_labels(soup)
    has_sourcey=any(x in labels for x in ['the sources','sources','source trail','receipts'])
    post_body=soup.select_one('.post-body')
    post_nav=soup.select_one('.post-nav')
    insertion_point=post_nav if post_nav else None
    if post_body and not has_sourcey:
        ext=collect_external_links(soup)
        if ext:
            items=''.join([f'<li><a href="{html.escape(href)}" target="_blank" rel="noopener">{html.escape(txt)}</a></li>' for txt,href in ext[:6]])
            block=make_note(soup,'Source Trail', f'<p>Primary links used or referenced in this post are collected here for faster verification.</p><ul>{items}</ul>')
        elif is_personal:
            block=make_note(soup,'Context', '<p>This is a first-person/personal post. It stays in the archive because it explains the point of view behind the reporting. For the site\'s sourcing standards, see <a href="/receipts">Receipts</a>. For the broader accountability archive, see <a href="/the-lies">The Lies</a> and <a href="/corruption">Corruption</a>.</p>')
        else:
            block=make_note(soup,'Reporting Standard', '<p>This post belongs to the accountability archive. For source methodology, court paper trails, and primary-document guidance, see <a href="/receipts">Receipts</a>. For related tracking pages, see <a href="/the-lies">The Lies</a> and <a href="/corruption">Corruption</a>.</p>')
        if insertion_point:
            insertion_point.insert_before(block)
        else:
            post_body.append(block)
        changed=True

    # add why it matters note for notably thin posts if absent
    labels=existing_note_labels(soup)
    wc=int(row['word_count']) if row is not None and not pd.isna(row['word_count']) else 999
    if post_body and wc < 340 and 'why it matters' not in labels:
        deck=extract_deck(soup)
        fp=first_body_paragraph(soup)
        summary=deck or fp
        if summary:
            msg=f'<p>{html.escape(trunc(summary, 210))} This matters because the site works best when each post makes the consequence explicit, not just the outrage. Use this post as a quick documented marker inside the larger archive.</p>'
            block=make_note(soup,'Why It Matters', msg)
            if post_nav:
                post_nav.insert_before(block)
            else:
                post_body.append(block)
            changed=True

    if changed:
        path.write_text(str(soup), encoding='utf-8')
        print('updated', path.name)
