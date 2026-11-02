# o'zim yozgan custome middleware:
from urllib import response


class SimpleMiddleware:
	def __init__(self, get_response):		# qanaqa ishlatilishi.
		self.get_response = get_response

	def __call__(self, request):		# nimaga ishlatilishi.
		# so'rov backend ga borishdan oldin nimadir qilish mumkin:
		# print(f"So'rov serverga borishdan oldin-Before Request For {request.path}")

		response = self.get_response(request)
		# javob backenddan brawzerga borishdan oldin nimadir qilish mumkin:
		# print("Javob klientga borishdan oldin-After Getting response")

		return response		# javobni qaytarib yuboryapmiz
