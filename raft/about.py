from django.utils.translation import gettext_lazy as _


about_us = {
    'mission': {
        'title': _('Our mission'),
        'id': 'mission',
        'content': [
            {
                'title': _('Our Story'),
                'text': _("RAFT was founded to fill the gap in Vietnam's web development market. Far too often, companies hope to expand to foreign markets to reach a new customer base, but struggle to find the developers who understand both Vietnamese and foreign markets. By employing Vietnamese and Western employees, RAFT helps you bridge that gap."),
                'img': 'mission_story.jpg'
            },
            {
                'title': _('Our Passion'),
                'text': _("We pride ourselves on producing secure and performant applications and strive to keep up with today's ever-changing technological landscape. For us, development is not just a job - it's a passion. We'll bring that level of dedication and attention to detail to all of the applications and deployments we undertake with you."),
                'img': 'mission_passion.jpg'
            },
            {
                'title': _('Our Future'),
                'text': _("Vietnam is one of the fastest-growing markets today, a trend that will undoubtedly continue into the future. RAFT helps connect businesses and consumers in Vietnam and abroad."),
                'img': 'mission_future.jpg'
            }
        ]
    },
    'steps': {
        'title': _('How it works'),
        'id': 'steps',
        'content': [
            {
                'title': _('Get in touch'),
                'description': _("Contact us via email or the link in the navigation bar. Feel free to add as much detail as you'd like."),
            },
            {
                'title': _('Receive a price and time estimate'),
                'description': _("We'll get back to you and offer an estimate of the time to complete your project as well as the total cost. We can adjust and negotiate at this stage, and add and subtract services until you're satisfied with the plan."),
            },
            {
                'title': _('Sign a contract'),
                'description': _("At this stage, you'll sign a contract with RAFT and pay the deposit to begin work on your application."),
            },
            {
                'title': _('Deployment'),
                'description': _("When development has finished on your application, we'll deploy it based on the agreed contractual terms and after receiving the final payment"),
            },
            {
                'title': _('More questions?'),
                'description': _("Feel free to reach out at any time to have RAFT answer your questions."),
            },
        ]
    }
}
