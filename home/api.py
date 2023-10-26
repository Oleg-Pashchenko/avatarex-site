from django.contrib.auth.decorators import login_required


@login_required
def database_mode_update(request):
    pass


@login_required
def knowledge_mode_update(request):
    pass


@login_required
def d_k_m_update(request):
    pass


@login_required
def prompt_mode_update(request):
    pass


@login_required
def database_mode_update_file_link(request):
    pass


@login_required
def knowledge_mode_update_file_link(request):
    pass


def d_k_m_update_database_link(request):
    pass


def d_k_m_update_knowledge_link(request):
    pass


def update_openai_key(request):
    pass

def sync_amo_pipelines(request):
    pass


def update_working_mode(request):
    pass


def get_stages_by_pipeline(request):
    pass

