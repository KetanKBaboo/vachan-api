'''GraphQL queries and mutations'''
#pylint: disable=too-many-lines
import graphene
import schemas
import schemas_nlp
import schema_auth
from routers import translation_apis , content_apis, auth_api
from crud import projects_crud,nlp_crud
from graphql_api import types, utils
from authentication import get_user_or_none_graphql
#Data classes and graphql classes have few methods
#pylint: disable=E1101,R1726,too-many-locals
############ ADD NEW Language #################
class AddLanguage(graphene.Mutation):
    """Mutation class for Add Language"""
    class Arguments:#pylint: disable=too-few-public-methods,E1101
        """Arguments declaration for the mutation"""
        language_addargs = types.InputAddLang(required=True)

    data = graphene.Field(types.Language)
    message = graphene.String()
#pylint: disable=R0201
    async def mutate(self,info,language_addargs):
        '''resolve'''
        db_ = info.context["request"].db_session
        #Auth and access rules
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/languages"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (language_addargs,schemas.LanguageCreate)
        response = await content_apis.add_language(request=req, lang_obj = schema_model,
        user_details=user_details, db_=db_)
        # result =structurals_crud.create_language(db_,lang=schema_model)
        result = response['data']
        language = types.Language(
                languageId = result.languageId,
                language = result.language,
                code = result.code,
                scriptDirection = result.scriptDirection,
                metaData = result.metaData
        )
        message = response['message']
        return AddLanguage(message=message,data=language)

############### Update Language ##############
class UpdateLanguage(graphene.Mutation):
    """ Mutation for update language"""
    class Arguments:#pylint: disable=too-few-public-methods
        """ Argumnets declare for mutations"""
        language_updateargs = types.InputUpdateLang(required=True)

    data = graphene.Field(types.Language)
    message = graphene.String()
#pylint: disable=R0201
    async def mutate(self,info,language_updateargs):
        """resolver"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = "/v2/languages"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (language_updateargs,schemas.LanguageEdit)
        response = await content_apis.edit_language(request=req, lang_obj = schema_model,
            user_details=user_details, db_=db_)
        result = response['data']
        language = types.Language(
                languageId = result.languageId,
                language = result.language,
                code = result.code,
                scriptDirection = result.scriptDirection,
                metaData = result.metaData
        )
        message = response['message']
        return UpdateLanguage(message=message,data=language)

############# Add Contents Type ###############
class CreateContentTypes(graphene.Mutation):
    """Mutation for Content types Creation"""
    class Arguments:#pylint: disable=too-few-public-methods
        "mutation arguments"
        content_type = types.InputContentType(required=True)

    data = graphene.Field(types.ContentType)
    message = graphene.String()
#pylint: disable=R0201
    async def mutate(self,info,content_type):
        """resolver"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/contents"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (content_type,schemas.ContentTypeCreate)
        response = await content_apis.add_contents(request=req,content=schema_model,
        user_details=user_details, db_=db_)
        result = response['data']
        content_type = types.ContentType(
            contentId = result.contentId,
            contentType = result.contentType
        )
        message =response['message']
        return CreateContentTypes(message = message, data = content_type)

########## Add License ########
#pylint: disable=too-few-public-methods
class AddLicense(graphene.Mutation):
    """Mutation class for Add Licenses"""
    class Arguments:
        """Arguments declaration for the mutation"""
        license_args = types.InputAddLicense(required=True)

    message = graphene.String()
    data = graphene.Field(types.License)
#pylint: disable=R0201
    async def mutate(self,info,license_args):
        '''resolve'''
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/licenses"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (license_args,schemas.LicenseCreate)
        response = await content_apis.add_license(request=req,license_obj=schema_model,
        user_details=user_details,db_=db_)
        result = response["data"]
        license_var = types.License(
            name = result.name,
            code = result.code,
            license = result.license,
            permissions = result.permissions,
            active = result.active
        )
        message = response['message']
        return AddLicense(message=message,data=license_var)

########## Edit License ########
#pylint: disable=too-few-public-methods
class EditLicense(graphene.Mutation):
    """Mutation class for Edit Licenses"""
    class Arguments:
        """Arguments declaration for the mutation"""
        license_args = types.InputEditLicense()

    message = graphene.String()
    data = graphene.Field(types.License)
#pylint: disable=R0201
    async def mutate(self,info,license_args):
        '''resolve'''
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = "/v2/licenses"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (license_args,schemas.LicenseEdit)
        response =await content_apis.edit_license(request=req,license_obj=schema_model,
            user_details=user_details, db_=db_)
        result = response['data']
        license_var = types.License(
            name = result.name,
            code = result.code,
            license = result.license,
            permissions = result.permissions,
            active = result.active
        )
        message = response['message']
        return AddLicense(message=message,data=license_var)

########## Add Version ########
class AddVersion(graphene.Mutation):
    "Mutations for Add Version"
    class Arguments:
        """Arguments for Add Version"""
        version_arg = types.InputAddVersion()

    message = graphene.String()
    data = graphene.Field(types.Version)
#pylint: disable=R0201
    async def mutate(self,info,version_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/versions"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (version_arg,schemas.VersionCreate)
        response = await content_apis.add_version(request=req, version_obj=schema_model,
            user_details=user_details, db_=db_)
        result =response['data']
        version_var = types.Version(
            versionId = result.versionId,
            versionAbbreviation = result.versionAbbreviation,
            versionName = result.versionName,
            revision = result.revision,
            metaData = result.metaData
        )
        message = response['message']
        return AddVersion(message=message,data=version_var)

########## Edit Version ########
class EditVersion(graphene.Mutation):
    "Mutations for Edit Version"
    class Arguments:
        """Arguments for Edit Version"""
        version_arg = types.InputEditVersion()

    message = graphene.String()
    data = graphene.Field(types.Version)
#pylint: disable=R0201
    async def mutate(self,info,version_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = "/v2/versions"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (version_arg,schemas.VersionEdit)
        response = await content_apis.edit_version(request=req, ver_obj=schema_model,
            user_details=user_details, db_=db_)
        result = response['data']
        version_var = types.Version(
            versionId = result.versionId,
            versionAbbreviation = result.versionAbbreviation,
            versionName = result.versionName,
            revision = result.revision,
            metaData = result.metaData
        )
        message = response['message']
        return EditVersion(message=message,data=version_var)

########## Add Source ########
class AddSource(graphene.Mutation):
    "Mutations for Add Source"
    class Arguments:
        """Arguments for Add Source"""
        source_arg = types.InputAddSource()

    message = graphene.String()
    data = graphene.Field(types.Source)
#pylint: disable=R0201
    async def mutate(self,info,source_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/sources"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (source_arg,schemas.SourceCreate)
        # source_name = schema_model.language + "_" + schema_model.version + "_" +\
        #     schema_model.revision + "_" + schema_model.contentType
        response = await content_apis.add_source(request=req,source_obj=schema_model,
        user_details=user_details, db_=db_)
        result = response['data']
        source_var = types.Source(
            sourceName = result.sourceName,
            contentType = result.contentType,
            language = result.language,
            version = result.version,
            year = result.year,
            license = result.license,
            metaData = result.metaData,
            active = result.active
        )
        message = response['message']
        return AddSource(message=message,data=source_var)

########## Edit Sources ########
class EditSource(graphene.Mutation):
    "Mutations for Edit Source"
    class Arguments:
        """Arguments for Edit Source"""
        source_arg = types.InputEditSource()

    message = graphene.String()
    data = graphene.Field(types.Source)
#pylint: disable=R0201
    async def mutate(self,info,source_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = "/v2/sources"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (source_arg,schemas.SourceEdit)
        response = await content_apis.edit_source(request=req, source_obj=schema_model,
        user_details=user_details, db_=db_)
        result = response['data']
        # result =structurals_crud.update_source(db_,schema_model,user_id = None)
        source_var = types.Source(
            sourceName = result.sourceName,
            contentType = result.contentType,
            language = result.language,
            version = result.version,
            year = result.year,
            license = result.license,
            metaData = result.metaData,
            active = result.active
        )
        message = response['message']
        return EditSource(message=message,data=source_var)

########## Add Bible books ########
class AddBible(graphene.Mutation):
    "Mutations for Add Bible"
    class Arguments:
        """Arguments for Add Bible"""
        bible_arg = types.InputAddBible()

    message = graphene.String()
    data = graphene.List(types.BibleContent)
#pylint: disable=no-self-use
    async def mutate(self,info,bible_arg):
        """resolve"""
        source =bible_arg.source_name
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = f"/v2/bibles/{source}/books"
        req.path_params["source_name"] = source
        books = bible_arg.books
        schema_list = []
        for item in books:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.BibleBookUpload)
            schema_list.append(schema_model)
        # result =contents_crud.upload_bible_books(db_=db_, source_name=source,
        # books=schema_list, user_id=None)
        response = await content_apis.add_bible_book(request= req,
            source_name = source, books = schema_list, user_details =user_details,
            db_ = db_)
        result = response['data']
        bible_content_list = []
        for item in result:
            bible_var = types.BibleContent(
            book = item.book,
            USFM = item.USFM,
            JSON = item.JSON,
            audio = item.audio,
            active = item.active
            )
            bible_content_list.append(bible_var)
        message = response['message']
        return AddBible(message=message,data=bible_content_list)

########## Edit Bible books ########
class EditBible(graphene.Mutation):
    "Mutations for Edit Bible"
    class Arguments:
        """Arguments for Edit Bible"""
        bible_arg = types.InputEditBible()

    message = graphene.String()
    data = graphene.List(types.BibleContent)
    #pylint: disable=no-self-use
    async def mutate(self,info,bible_arg):
        """resolve"""
        source =bible_arg.source_name
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = f"/v2/bibles/{source}/books"
        req.path_params["source_name"] = source
        books = bible_arg.books
        schema_list = []
        for item in books:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.BibleBookEdit)
            schema_list.append(schema_model)
        # result =contents_crud.update_bible_books(db_=db_, source_name=source,
        # books=schema_list, user_id=None)
        response = await content_apis.edit_bible_book(request= req,
            source_name = source, books = schema_list, user_details =user_details,
            db_ = db_)
        result = response['data']
        bible_content_list = []
        for item in result:
            bible_var = types.BibleContent(
            book = item.book,
            USFM = item.USFM,
            JSON = item.JSON,
            audio = item.audio,
            active = item.active
            )
            bible_content_list.append(bible_var)
        message = response['message']
        return EditBible(message=message,data=bible_content_list)

########## Add Audio bible ########
class AddAudioBible(graphene.Mutation):
    "Mutations for Add Audio Bible"
    class Arguments:
        """Arguments for Add Audio Bible"""
        audio_bible_arg = types.InputAddAudioBible()

    message = graphene.String()
    data = graphene.List(types.AudioBible)
#pylint: disable=R0201
    async def mutate(self,info,audio_bible_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =audio_bible_arg.source_name
        audio_data = audio_bible_arg.audio_data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = f"/v2/bibles/{source}/audios"
        req.path_params["source_name"] = source
        schema_list = []
        for item in audio_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.AudioBibleUpload)
            schema_list.append(schema_model)
        # result =contents_crud.upload_bible_audios(db_=db_, source_name=source,
        # audios=schema_list, user_id=None)
        response = await content_apis.add_audio_bible(request=req,
            source_name=source, audios=schema_list, user_details=user_details,
            db_=db_)
        result = response['data']
        audio_content_list = []
        for item in result:
            audio_var = types.AudioBible(
            name = item.name,
            url = item.url,
            format = item.format,
            active = item.active
            )
            audio_content_list.append(audio_var)
        message = response['message']
        return AddAudioBible(message=message,data=audio_content_list)

########## Edit Audio bible ########
class EditAudioBible(graphene.Mutation):
    "Mutations for Edit Audio Bible"
    class Arguments:
        """Arguments for Edit Audio Bible"""
        audio_bible_arg = types.InputEditAudioBible()

    message = graphene.String()
    data = graphene.List(types.AudioBible)
#pylint: disable=no-self-use
    async def mutate(self,info,audio_bible_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =audio_bible_arg.source_name
        audio_data = audio_bible_arg.audio_data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = f"/v2/bibles/{source}/audios"
        req.path_params["source_name"] = source
        schema_list = []
        for item in audio_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.AudioBibleEdit)
            schema_list.append(schema_model)
        # result =contents_crud.update_bible_audios(db_=db_, source_name=source,
        # audios=schema_list, user_id=None)
        response = await content_apis.edit_audio_bible(request=req,
            source_name=source, audios=schema_list, user_details=user_details,
            db_=db_)
        result = response['data']
        audio_content_list = []
        for item in result:
            audio_var = types.AudioBible(
            name = item.name,
            url = item.url,
            format = item.format,
            active = item.active
            )
            audio_content_list.append(audio_var)
        message = response['message']
        return EditAudioBible(message=message,data=audio_content_list)

########## Add Commentaries ########
class AddCommentary(graphene.Mutation):
    "Mutations for Add Commentary"
    class Arguments:
        """Arguments for Add Commentary"""
        comm_arg = types.InputAddCommentary()

    message = graphene.String()
    data = graphene.List(types.Commentary)
#pylint: disable=no-self-use
    async def mutate(self,info,comm_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =comm_arg.source_name
        comm_data = comm_arg.commentary_data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = f"/v2/commentaries/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in comm_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.CommentaryCreate)
            schema_list.append(schema_model)
        # result =contents_crud.upload_commentaries(db_=db_, source_name=source,
        # commentaries=schema_list, user_id=None)
        response = await content_apis.add_commentary(request=req,
            source_name=source,commentaries= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        comm_content_list = []
        for item in result:
            comm_var = types.Commentary(
                book = item.book,
                chapter = item.chapter,
                verseStart = item.verseStart,
                verseEnd = item.verseEnd,
                commentary = item.commentary,
                active = item.active
            )
            comm_content_list.append(comm_var)
        message = response['message']
        return AddCommentary(message=message,data=comm_content_list)

########## Edit Commentaries #######
class EditCommentary(graphene.Mutation):
    "Mutations for Edit Commentary"
    class Arguments:
        """Arguments for Edit Commentary"""
        comm_arg = types.InputEditCommentary()

    message = graphene.String()
    data = graphene.List(types.Commentary)
#pylint: disable=no-self-use
    async def mutate(self,info,comm_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =comm_arg.source_name
        comm_data = comm_arg.commentary_data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = f"/v2/commentaries/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in comm_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.CommentaryEdit)
            schema_list.append(schema_model)
        # result =contents_crud.update_commentaries(db_=db_, source_name=source,
        # commentaries=schema_list, user_id=None)
        response = await content_apis.edit_commentary(request=req,
            source_name=source,commentaries= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        comm_content_list = []
        for item in result:
            comm_var = types.Commentary(
                book = item.book,
                chapter = item.chapter,
                verseStart = item.verseStart,
                verseEnd = item.verseEnd,
                commentary = item.commentary,
                active = item.active
            )
            comm_content_list.append(comm_var)
        message = response['message']
        return EditCommentary(message=message,data=comm_content_list)

##### AGMT PROJECT MANAGEMENT Create #######
class CreateAGMTProject(graphene.Mutation):
    "Mutations for CreateAGMTProject"
    class Arguments:
        """Arguments for CreateAGMTProject"""
        project_arg = types.InputCreateAGMTProject()

    message = graphene.String()
    data = graphene.Field(types.TranslationProject)
#pylint: disable=no-self-use
    async def mutate(self,info,project_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/autographa/projects"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (project_arg,schemas_nlp.TranslationProjectCreate)
        response = await translation_apis.create_project(request=req,
        project_obj=schema_model,user_details=user_details,db_=db_)
        result = response['data']
        comm = types.TranslationProject(
            projectId = result.projectId,
            projectName = result.projectName,
            sourceLanguage = result.sourceLanguage,
            targetLanguage = result.targetLanguage,
            documentFormat = result.documentFormat,
            users = result.users,
            metaData = result.metaData,
            active = result.active
        )
        message = response['message']
        return CreateAGMTProject(message = message, data = comm)

##### AGMT PROJECT MANAGEMENT EDIT #######
class EditAGMTProject(graphene.Mutation):
    "Mutations for EditAGMTProject"
    class Arguments:
        """Arguments for EditAGMTProject"""
        project_arg = types.InputEditAGMTProject()

    message = graphene.String()
    data = graphene.Field(types.TranslationProject)
#pylint: disable=no-self-use
    async def mutate(self,info,project_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req = info.context['request']
        req.scope['method'] = "PUT"
        req.scope['path'] = "/v2/autographa/projects"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (project_arg,schemas_nlp.TranslationProjectEdit)

        result = await translation_apis.update_project(
            request=req, project_obj=schema_model, 
            user_details= user_details, db_=db_)
        message = result["message"]
        comm = result["data"]
        return EditAGMTProject(message = message, data = comm)

##### AGMT project user #######
class AGMTUserCreate(graphene.Mutation):
    """mutation for AGMT user create"""
    class Arguments:
        """args"""
        user_arg = types.AGMTUserCreateInput()

    message = graphene.String()
    data = graphene.Field(types.ProjectUser)
#pylint: disable=no-self-use
    async def mutate(self,info,user_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        project_id = user_arg.project_id
        user_id = user_arg.user_id
        user_details , req = get_user_or_none_graphql(info)
        req = info.context['request']
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/autographa/project/user"
        response = await translation_apis.add_user(request=req,
            project_id=project_id, user_id=user_id,
            user_details=user_details, db_=db_)
        result = response['data']
        comm = types.ProjectUser(
            project_id = result.project_id,
            userId = result.userId,
            userRole = result.userRole,
            metaData = result.metaData,
            active = result.active
        )
        message = response['message']
        return AGMTUserCreate(message = message, data = comm)

##### AGMT project user Edit #######
class AGMTUserEdit(graphene.Mutation):
    """mutation for AGMT user Edit"""
    class Arguments:
        """args"""
        user_arg = types.AGMTUserEditInput()

    message = graphene.String()
    data = graphene.Field(types.ProjectUser)
#pylint: disable=no-self-use
    async def mutate(self,info,user_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        user_details , req = get_user_or_none_graphql(info)
        req = info.context['request']
        req.scope['method'] = "PUT"
        req.scope['path'] = "/v2/autographa/project/user"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (user_arg,schemas_nlp.ProjectUser)
        response = await translation_apis.update_user(request=req,
            user_obj=schema_model, user_details=user_details, db_=db_)
        result = response['data']
        comm = types.ProjectUser(
            project_id = result.project_id,
            userId = result.userId,
            userRole = result.userRole,
            metaData = result.metaData,
            active = result.active
        )
        message = response['message']
        return AGMTUserEdit(message = message, data = comm)

########## Add BibleVideo ########
class AddBibleVideo(graphene.Mutation):
    "Mutations for Add BibleVideo"
    class Arguments:
        """Arguments for Add BibleVideo"""
        video_arg = types.InputAddBibleVideo()

    message = graphene.String()
    data = graphene.List(types.BibleVideo)
#pylint: disable=no-self-use
    async def mutate(self,info,video_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =video_arg.source_name
        video_data = video_arg.video_data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = f"/v2/biblevideos/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in video_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.BibleVideoUpload)
            schema_list.append(schema_model)
        # result =contents_crud.upload_bible_videos(db_=db_, source_name=source,
        # videos=schema_list, user_id=None)
        response = await content_apis.add_biblevideo(request=req,
            source_name=source,videos= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        video_content_list = []
        for item in result:
            comm_var = types.BibleVideo(
                title = item.title,
                books = item.books,
                videoLink = item.videoLink,
                description = item.description,
                theme = item.theme,
                active = item.active
            )
            video_content_list.append(comm_var)
        message = response['message']
        return AddBibleVideo(message=message,data=video_content_list)

########## Edit BibleVideo ########
class EditBibleVideo(graphene.Mutation):
    "Mutations for Edit BibleVideo"
    class Arguments:
        """Arguments for Edit BibleVideo"""
        video_arg = types.InputEditBibleVideo()

    message = graphene.String()
    data = graphene.List(types.BibleVideo)
#pylint: disable=no-self-use
    async def mutate(self,info,video_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =video_arg.source_name
        video_data = video_arg.video_data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = f"/v2/biblevideos/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in video_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.BibleVideoEdit)
            schema_list.append(schema_model)
        # result =contents_crud.update_bible_videos(db_=db_, source_name=source,
        # videos=schema_list, user_id=None)
        response = await content_apis.edit_biblevideo(request=req,
            source_name=source,videos= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        video_content_list = []
        for item in result:
            comm_var = types.BibleVideo(
                title = item.title,
                books = item.books,
                videoLink = item.videoLink,
                description = item.description,
                theme = item.theme,
                active = item.active
            )
            video_content_list.append(comm_var)
        message = response['message']
        return EditBibleVideo(message=message,data=video_content_list)

############# Add Dictionary ###############
class AddDictionary(graphene.Mutation):
    "Mutations for Add Dictionary"
    class Arguments:
        """Arguments for Add Dictionary"""
        dict_arg = types.InputAddDictionary()

    message = graphene.String()
    data = graphene.List(types.DictionaryWord)
#pylint: disable=no-self-use
    async def mutate(self,info,dict_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =dict_arg.source_name
        dict_data = dict_arg.word_list
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = f"/v2/dictionaries/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in dict_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.DictionaryWordCreate)
            schema_list.append(schema_model)
        # result =contents_crud.upload_dictionary_words(db_=db_, source_name=source,
        # dictionary_words=schema_list, user_id=None)
        response = await content_apis.add_dictionary_word(request=req,
            source_name=source, dictionary_words= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        dict_content_list = []
        for item in result:
            dict_var = types.DictionaryWord(
                word = item.word,
                details = item.details,
                active = item.active
            )
            dict_content_list.append(dict_var)
        message = response['message']
        return AddDictionary(message=message,data=dict_content_list)

########## Edit Dictionary ########
class EditDictionary(graphene.Mutation):
    "Mutations for Edit Dictionary"
    class Arguments:
        """Arguments for Add Dictionary"""
        dict_arg = types.InputEditDictionary()

    message = graphene.String()
    data = graphene.List(types.DictionaryWord)
#pylint: disable=no-self-use
    async def mutate(self,info,dict_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =dict_arg.source_name
        dict_data = dict_arg.word_list
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = f"/v2/dictionaries/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in dict_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.DictionaryWordEdit)
            schema_list.append(schema_model)
        # result =contents_crud.update_dictionary_words(db_=db_, source_name=source,
        # dictionary_words=schema_list, user_id=None)
        response = await content_apis.edit_dictionary_word(request=req,
            source_name=source, dictionary_words= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        dict_content_list = []
        for item in result:
            dict_var = types.DictionaryWord(
                word = item.word,
                details = item.details,
                active = item.active
            )
            dict_content_list.append(dict_var)
        message = response['message']
        return EditDictionary(message=message,data=dict_content_list)

########## Add Infographics ########
class AddInfographic(graphene.Mutation):
    "Mutations for Add Infographic"
    class Arguments:
        """Arguments for Add Infographic"""
        info_arg = types.InputAddInfographic()

    message = graphene.String()
    data = graphene.List(types.Infographic)
#pylint: disable=no-self-use
    async def mutate(self,info,info_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =info_arg.source_name
        dict_data = info_arg.data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = f"/v2/infographics/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in dict_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.InfographicCreate)
            schema_list.append(schema_model)
        response = await content_apis.add_infographics(request=req,
            source_name=source, infographics= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        dict_content_list = []
        for item in result:
            dict_var = types.Infographic(
                book = item.book,
                title = item.title,
                infographicLink = item.infographicLink,
                active = item.active
            )
            dict_content_list.append(dict_var)
        message = response['message']
        return AddInfographic(message=message,data=dict_content_list)

########## Edit Infographics ########
class EditInfographic(graphene.Mutation):
    "Mutations for Edit Infographic"
    class Arguments:
        """Arguments for Edit Infographic"""
        info_arg = types.InputEditInfographic()

    message = graphene.String()
    data = graphene.List(types.Infographic)
#pylint: disable=no-self-use
    async def mutate(self,info,info_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source =info_arg.source_name
        dict_data = info_arg.data
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = f"/v2/infographics/{source}"
        req.path_params["source_name"] = source
        schema_list = []
        for item in dict_data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas.InfographicEdit)
            schema_list.append(schema_model)
        # result =contents_crud.update_infographics(db_=db_, source_name=source,
        # infographics=schema_list, user_id=None)
        response = await content_apis.edit_infographics(request=req,
            source_name=source, infographics= schema_list,
            user_details=user_details, db_=db_)
        result = response['data']
        dict_content_list = []
        for item in result:
            dict_var = types.Infographic(
                book = item.book,
                title = item.title,
                infographicLink = item.infographicLink,
                active = item.active
            )
            dict_content_list.append(dict_var)
        message = response['message']
        return EditInfographic(message=message,data=dict_content_list)

########## Autographa - Translation ########
# Apply token translation
class AgmtTokenApply(graphene.Mutation):
    "Mutations for  Token apply"
    class Arguments:
        """Arguments for Token apply"""
        token_arg = types.InputApplyToken()

    message = graphene.String()
    data = graphene.List(types.Sentence)
#pylint: disable=no-self-use
    def mutate(self,info,token_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        project_id = token_arg.project_id
        return_drafts = token_arg.return_drafts
        token = token_arg.token

        schema_list = []
        for item in token:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas_nlp.TokenUpdate)
            schema_list.append(schema_model)
        result = nlp_crud.save_agmt_translations(db_=db_,project_id=project_id,\
            token_translations = schema_list,return_drafts = return_drafts,user_id=None)
        dict_content_list = []
        for item in result:
            comm = types.Sentence(
            sentenceId = item.sentenceId,
            sentence = item.sentence,
            draft = item.draft,
            draftMeta = item.draftMeta
            )
            dict_content_list.append(comm)
        message = "Token translations saved"
        return AgmtTokenApply(message=message,data=dict_content_list)

#### Translation Suggetions ##########
#Suggeest Auto Translation
class AutoTranslationSuggetion(graphene.Mutation):
    "Mutations for AutoTranslationSuggetion"
    class Arguments:
        """Arguments for AutoTranslationSuggetion"""
        translation_arg = types.InputAutoTranslation()

    Output = graphene.List(types.Sentence)
#pylint: disable=no-self-use
    def mutate(self,info,translation_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        project_id  = translation_arg.project_id
        books = translation_arg.books
        sentence_id_list = translation_arg.sentence_id_list
        sentence_id_range = translation_arg.sentence_id_range
        confirm_all = translation_arg.confirm_all

        result =nlp_crud.agmt_suggest_translations(db_=db_,project_id=project_id,books=books,\
            sentence_id_list=sentence_id_list,sentence_id_range=sentence_id_range,\
            confirm_all=confirm_all)

        dict_content_list = []
        for item in result:
            comm = types.Sentence(
            sentenceId = item.sentenceId,
            sentence = item.sentence,
            draft = item.draft,
            draftMeta = item.draftMeta
            )
            dict_content_list.append(comm)
        return dict_content_list

############### Add Gloss ##############
class AddGloss(graphene.Mutation):
    "Mutations for AddGloss"
    class Arguments:
        """Arguments for AddGloss"""
        gloss_arg = types.InputAddGloss()

    message = graphene.String()
    data = graphene.List(types.Gloss)
#pylint: disable=no-self-use
    def mutate(self,info,gloss_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source_language = gloss_arg.source_language
        target_language =gloss_arg.target_language
        schema_list = []
        for item in gloss_arg.data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas_nlp.GlossInput)
            schema_list.append(schema_model)

        result =nlp_crud.add_to_translation_memory(db_=db_,src_lang=source_language,\
           trg_lang=target_language,gloss_list=schema_list)

        dict_content_list = []
        for item in result:
            if 'translations' and  'metaData' in item:
                dict_var = types.Gloss(
               token = item["token"],
               translations = item["translations"],
               metaData = item["metaData"]
            )
            elif "translations" in item:
                dict_var = types.Gloss(
               token = item["token"],
               translations = item["translations"]
            )
            elif "metaData" in item:
                dict_var = types.Gloss(
               token = item["token"],
               metaData = item["metaData"]
            )

            dict_content_list.append(dict_var)
        message = "Added to glossary"
        return AddGloss(message=message,data=dict_content_list)

############### Add Alignment
class AddAlignment(graphene.Mutation):
    "Mutations for AddAlignment"
    class Arguments:
        """Arguments for AddAlignment"""
        alignment_arg = types.InputAddAlignment()

    message = graphene.String()
    data = graphene.List(types.Gloss)
#pylint: disable=no-self-use
    def mutate(self,info,alignment_arg):
        """resolve"""
        db_ = info.context["request"].db_session
        source_language = alignment_arg.source_language
        target_language =alignment_arg.target_language
        schema_list = []
        for item in alignment_arg.data:
            schema_model = utils.convert_graphene_obj_to_pydantic\
            (item,schemas_nlp.Alignment)
            schema_list.append(schema_model)

        result =nlp_crud.alignments_to_trainingdata(db_=db_,src_lang=source_language,\
            trg_lang=target_language,alignment_list=schema_list,user_id=20202)

        dict_content_list = []
        for item in result:
            if "translations" and  "metaData" in item:
                dict_var = types.Gloss(
               token = item["token"],
               translations = item["translations"],
               metaData = item["metaData"]
            )
            elif "translations" in item:
                dict_var = types.Gloss(
               token = item["token"],
               translations = item["translations"]
            )
            elif "metaData" in item:
                dict_var = types.Gloss(
               token = item["token"],
               metaData = item["metaData"]
            )

            dict_content_list.append(dict_var)
        message = "Added to Alignments"
        return AddAlignment(message=message,data=dict_content_list)

######################### Authentication ############################
#Register
class Register(graphene.Mutation):
    """Mutation class for Register User"""
    class Arguments:#pylint: disable=too-few-public-methods,E1101
        """Arguments declaration for the mutation"""
        app_type = types.App(default_value=types.App.API.value)
        registration_args = types.RegisterInput()

    registered_details = graphene.Field(types.RegisterResponse)
    message = graphene.String()
    token  = graphene.String()
#pylint: disable=R0201
    async def mutate(self,info,registration_args,app_type):
        '''resolve'''
        db_ = info.context["request"].db_session
        #Auth and access rules
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "POST"
        req.scope['path'] = "/v2/user/register"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (registration_args,schema_auth.Registration)
        response = await auth_api.register(request=req, register_details = schema_model,
        user_details=user_details, db_=db_, app_type = app_type)
        result = response['registered_details']
        register = types.RegisterResponse(
                id = result['id'],
                email = result['email'],
                permissions = result['Permissions']
        )
        message = response['message']
        token = response['token'] if "token" in response else ""
        return Register(message=message,registered_details=register,token = token)

#User Role update
class UpdateUserRole(graphene.Mutation):
    """Mutation class for Update User role"""
    class Arguments:#pylint: disable=too-few-public-methods,E1101
        """Arguments declaration for the mutation"""
        user_roles_args = types.UserroleInput()

    message = graphene.String()
    role_list = graphene.List(types.AdminRoles)
#pylint: disable=R0201
    async def mutate(self,info,user_roles_args):
        '''resolve'''
        db_ = info.context["request"].db_session
        #Auth and access rules
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "PUT"
        req.scope['path'] = "/v2/user/userrole"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (user_roles_args,schema_auth.UserRole)
        response = await auth_api.userrole(request=req, role_data = schema_model,
        user_details=user_details, db_=db_)
        message = response['message']
        return UpdateUserRole(message=message,role_list=response["role_list"])

#User identity delete
class DeleteIdentity(graphene.Mutation):
    """Mutation class for delete identiy of user"""
    class Arguments:#pylint: disable=too-few-public-methods,E1101
        """Arguments declaration for the mutation"""
        identity = types.UserIdentity()

    message = graphene.String()
#pylint: disable=R0201
    async def mutate(self,info,identity):
        '''resolve'''
        db_ = info.context["request"].db_session
        #Auth and access rules
        user_details , req = get_user_or_none_graphql(info)
        req.scope['method'] = "DELETE"
        req.scope['path'] = "/v2/user/delete-identity"
        schema_model = utils.convert_graphene_obj_to_pydantic\
            (identity,schema_auth.UserIdentity)
        response = await auth_api.delete_user(request=req, user = schema_model,
        user_details=user_details, db_=db_)
        message = response["message"]
        return DeleteIdentity(message= message)

########## ALL MUTATIONS FOR API ########
class VachanMutations(graphene.ObjectType):
    '''All defined mutations'''
    add_language = AddLanguage.Field()
    update_language = UpdateLanguage.Field()
    add_content_type = CreateContentTypes.Field()
    add_license = AddLicense.Field()
    edit_license = EditLicense.Field()
    add_version = AddVersion.Field()
    edit_version = EditVersion.Field()
    add_source = AddSource.Field()
    edit_source = EditSource.Field()
    add_bible_book = AddBible.Field()
    edit_bible_book = EditBible.Field()
    add_audio_bible = AddAudioBible.Field()
    edit_audio_bible = EditAudioBible.Field()
    add_commentary = AddCommentary.Field()
    edit_commentary = EditCommentary.Field()
    add_bible_video = AddBibleVideo.Field()
    edit_bible_video = EditBibleVideo.Field()
    add_dictionary = AddDictionary.Field()
    edit_dictionary = EditDictionary.Field()
    add_infographic = AddInfographic.Field()
    edit_infographic = EditInfographic.Field()
    create_agmt_project = CreateAGMTProject.Field()
    edit_agmt_project = EditAGMTProject.Field()
    create_agmt_project_user = AGMTUserCreate.Field()
    edit_agmt_project_user = AGMTUserEdit.Field()
    apply_agmt_token_translation = AgmtTokenApply.Field()
    suggest_agmt_auto_translation = AutoTranslationSuggetion.Field()
    #suggest_translation = TranslationSuggetion.Field()
    add_gloss = AddGloss.Field()
    add_alignment = AddAlignment.Field()
    register = Register.Field()
    update_userrole = UpdateUserRole.Field()
    delete_identity = DeleteIdentity.Field()
