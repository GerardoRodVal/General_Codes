httperrors
==========

Http errors provide a list of easy to test and descriptive set of python
errors.

Code example
------------

Raising exception
~~~~~~~~~~~~~~~~~

::

   from httperrors import BadRequestError
   class View(BaseView):
       def validate(self, request):
           ... 
           if not request.body.is_json():
               raise BadRequestError(
                   error_message="You must provide a JSON body",
                   error_code="NOT_A_JSON_BODY_ERROR",
               )
       def run(self,request):
           ...

Serialization
~~~~~~~~~~~~~

You will be able to catch this exception somewhere in the flow of your
application, map it and serialize it to the corresponding request.

::

   from httperrors import BadRequestError
   class BaseView:
   def __init__(self):
       try:
           self.validate()
       except BadRequestError as e:
           return json_response(
               status_code=e.status_code,
               body=e.serialize()
           )

Testing
~~~~~~~

You will be able to easily test your application

::

   from httperrors import BadRequestError
   class TestView:
   def test_it_raises_bad_request_error_not_json_body(self):
       view = View()
       request = Mock()
       request.body.is_json.return_value = False
       with pytest.raises(BadRequestError) as error:
           view.validate()
           assert error.error_code == "NOT_A_JSON_BODY_ERROR"

