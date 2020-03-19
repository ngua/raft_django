from django.utils.translation import gettext_lazy as _


slider = [
    {
        'name': 'WEB APPS AND SERVICES',
        'header': 'Choose from our range of web services:',
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
                'name': '...and more',
                'icon': 'more'
            }
        ],
        'href': '#',
        'link': _('Explore')
    },
    {
        'name': 'SERVICE',
        'header': 'What you get when you choose RAFT:',
        'content': [
            {
                'name': _('Source code'),
                'icon': 'code'
            },
            {
                'name': 'Seamless deployment',
                'icon': 'server'
            },
            {
                'name': 'Long-term maintenance and support',
                'icon': 'future'
            },
            {
                'name': 'Access control',
                'icon': 'users'
            },
            {
                'name': 'Security and encryption',
                'icon': 'lock'
            },
            {
                'name': 'Customization to meet your needs',
                'icon': 'settings'
            },
            {
                'name': 'Bilingual development',
                'icon': 'comments'
            },
            {
                'name': 'Quality, performant code',
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
        'desc': 'Reach New Customers and Expand Your Business',
        'img': 'langs.png',
        'href': 'web',
        'sub': [
            {
                'title': 'Built with Modern Languages',
                'desc': 'RAFT builds applications using only the most performant, safe, and modern technologies.'
            },
            {
                'title': 'Scalable Architecture',
                'desc': "Even if you're just starting out, RAFT build with future expansion in mind."
            },
            {
                'title': 'Bilingual Development',
                'desc': "RAFT employs native Vietnamese and English speakers to help you reach the widest possible audience at home and abroad. Don't let poor translations stand in the way of your success."
            },
            {
                'title': 'Easy Deployment',
                'desc': "RAFT takes care of your application's deployment and maintenance, and works with you to find the best solution for your business."
            }
        ]
    },
    {
        'title': _('Deployment'),
        'desc': 'Reliable and Scalable Builds',
        'img': 'deploy.png',
        'href': 'deployment',
        'sub': [
            {
                'title': 'Support and Administration',
                'desc': 'RAFT will work with you to deploy your application to cloud servers. Once your app is up and running, RAFT will continue to take care of the administration and maintenance of your app.'
            },
            {
                'title': 'Containerization',
                'desc': "Increase your app's portability by choosing RAFT's containerization service."
            },
            {
                'title': 'Domain Name Registration',
                'desc': 'RAFT takes care of the purchase and registration of your custom domain name.'
            },
            {
                'title': 'SSL Certification',
                'desc': 'All of our web applications come with free SSL certification to encrypt traffic to and from your server.'
            }
        ]
    },
    {
        'title': '...And More',
        'desc': 'More Services to Meet Your Needs',
        'img': 'other.png',
        'href': 'additional',
        'sub': [
            {
                'title': 'Source Code Included',
                'desc': "RAFT provides you with all of your app's source code, free of charge, for easy transfer and reproduction."
            },
            {
                'title': 'Data Management',
                'desc': 'Choose from relational databases including MySQL and PostgreSQL or NoSQL solutions, including Redis, MongoDB, and more.'
            },
            {
                'title': 'On-Site Training',
                'desc': 'If your team requires training in additional technical skills, RAFT can help train them in Git, Vim, and the Linux command line.'
            }
        ]
    }
]
