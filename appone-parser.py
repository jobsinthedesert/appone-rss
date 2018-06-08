import argparse
import feedparser

def search_jobs(url):
    """
    Returns job name and link for table within page
    """
    feed = feedparser.parse(url)

    jobs_list = []

    for job in feed.entries:
        entry = [job.link, job.title]
        jobs_list.append(entry)

    return jobs_list

def format_element(job, opening_tag, closing_tag):
    """
    Formats <link> and <title> elements
    """
    return('    '+opening_tag+job+closing_tag+'\n')

def format_item(title, link):
    """
    Joins <title> and <link> elements as children of <item>
    """
    return('  <item>\n'+title+link+'  </item>\n')

def sanitize_string(title):
    """
    Alters forbidden chracters in XML
    """
    clean_amp = title.replace('&', '&amp;')
    clean_quot = clean_amp.replace('"', '&quot;')
    clean_apos = clean_quot.replace('\'', '&apos;')
    clean_lt = clean_apos.replace('<', '&lt;')
    clean_gt = clean_lt.replace('>', '&gt;')

    clean_title = clean_gt

    return clean_title

def format_jobs(jobs):
    """
    Concatenates a string to return a list of jobs as <item> elems
    """

    job_item_string = ''

    for job in jobs:
        job_name = sanitize_string(job[1])
        title = format_element(job_name, '<title>', '</title>')
        link_parsed = sanitize_string(job[0])
        link = format_element(link_parsed, '<link>', '</link>')
        item = format_item(title, link)
        job_item_string += item

    return job_item_string

def format_rss(jobs, title, link):
    """
    Returns an RSS feed as a string
    """
    xml_opening = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    rss_opening = '<rss version="2.0">\n\n'
    channel_opening = '<channel>\n'
    
    channel_title = '  <title>'+title+'</title>\n'
    channel_link = '  <link>'+link+'</link>\n'

    header = xml_opening + rss_opening + channel_opening + channel_title + channel_link

    job_items = format_jobs(jobs)

    channel_closing = '</channel>\n'
    rss_closing = '</rss>'

    closing = channel_closing + rss_closing

    rss_feed = header + job_items + closing

    return rss_feed

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-url', required=True, help="edjoin url")
    parser.add_argument('-output', required=True, help="name of rss file ex: feed.xml")
    parser.add_argument('-title', required=True, help="name in RSS feed <title> tag")
    parser.add_argument('-link', required=True, help="location in RSS feed <link> tag")

    args = parser.parse_args()

    jobs = search_jobs(args.url)
    rss_feed = format_rss(jobs, args.title, args.link)

    with open(args.output, 'w+') as f:
        f.write(rss_feed)

if __name__ == '__main__':
    main()
