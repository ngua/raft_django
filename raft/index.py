from django.utils.translation import gettext_lazy as _


slider = [
    {
        'name': _('WEB APPS AND SERVICES'),
        'header': _('Choose from our range of web services:'),
        'content': [
            {
                'name': 'Blog',
                'icon': 'file-text'
            },
            {
                'name': 'eCommerce',
                'icon': 'cart'
            },
            {
                'name': _('Media'),
                'icon': 'video-camera'
            },
            {
                'name': _('Education'),
                'icon': 'file-edit'
            },
            {
                'name': 'REST API',
                'icon': 'cog'
            },
            {
                'name': _('...and more'),
                'icon': 'more'
            }
        ],
        'href': '#',
        'link': _('Explore')
    },
    {
        'name': _('SERVICE'),
        'header': _('What you get when you choose RAFT:'),
        'content': [
            {
                'name': _('Source code'),
                'icon': 'code'
            },
            {
                'name': _('Seamless deployment'),
                'icon': 'server'
            },
            {
                'name': _('Long-term maintenance and support'),
                'icon': 'future'
            },
            {
                'name': _('Access control'),
                'icon': 'users'
            },
            {
                'name': _('Security and encryption'),
                'icon': 'lock'
            },
            {
                'name': _('Customization to meet your needs'),
                'icon': 'settings'
            },
            {
                'name': _('Bilingual development'),
                'icon': 'comments'
            },
            {
                'name': _('Quality, performant code'),
                'icon': 'check'
            }
        ],
        'href': '#',
        'link': _('Explore')
    }
]

switcher = [
    {
        'title': _('Web Apps'),
        'desc': _('Reach New Customers and Expand Your Business'),
        'img': 'langs.png',
        'href': 'web',
        'sub': [
            {
                'title': _('Built with Modern Languages'),
                'desc': _('RAFT builds applications using only the most performant, safe, and modern technologies.')
            },
            {
                'title': _('Scalable Architecture'),
                'desc': _("Even if you're just starting out, RAFT build with future expansion in mind.")
            },
            {
                'title': _('Bilingual Development'),
                'desc': _("RAFT employs native Vietnamese and English speakers to help you reach the widest possible audience at home and abroad. Don't let poor translations stand in the way of your success.")
            },
            {
                'title': _('Easy Deployment'),
                'desc': _("RAFT takes care of your application's deployment and maintenance, and works with you to find the best solution for your business.")
            }
        ]
    },
    {
        'title': _('Deployment'),
        'desc': _('Reliable and Scalable Builds'),
        'img': 'deploy.png',
        'href': 'deployment',
        'sub': [
            {
                'title': _('Support and Administration'),
                'desc': _('RAFT will work with you to deploy your application to cloud servers. Once your app is up and running, RAFT will continue to take care of the administration and maintenance of your app.')
            },
            {
                'title': _('Containerization'),
                'desc': _("Increase your app's portability by choosing RAFT's containerization service.")
            },
            {
                'title': _('Domain Name Registration'),
                'desc': _('RAFT takes care of the purchase and registration of your custom domain name.')
            },
            {
                'title': _('SSL Certification'),
                'desc': _('All of our web applications come with free SSL certification to encrypt traffic to and from your server.')
            }
        ]
    },
    {
        'title': _('...And More'),
        'desc': _('More Services to Meet Your Needs'),
        'img': 'other.png',
        'href': 'additional',
        'sub': [
            {
                'title': _('Source Code Included'),
                'desc': _("RAFT provides you with all of your app's source code, free of charge, for easy transfer and reproduction.")
            },
            {
                'title': _('Data Management'),
                'desc': _('Choose from relational databases including MySQL and PostgreSQL or NoSQL solutions, including Redis, MongoDB, and more.')
            },
            {
                'title': _('On-Site Training'),
                'desc': _('If your team requires training in additional technical skills, RAFT can help train them in Git, Vim, and the Linux command line.')
            }
        ]
    }
]
