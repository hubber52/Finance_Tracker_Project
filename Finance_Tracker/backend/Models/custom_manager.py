from django.db import models

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_total(self, field:str, ruser, amount:str):
        rateType = field + "_rate"
        #Field in format "", amount in format "_"
        amountType = field + amount

        week_totals = self.get_queryset().filter(user=ruser, 
                                                 **{rateType : "Weekly"})
        month_totals = self.get_queryset().filter(user=ruser, 
                                                  **{rateType : "Monthly"})
        year_totals = self.get_queryset().filter(user=ruser, 
                                                 **{rateType : "Annually"})
        week_sum, month_sum, year_sum = 0, 0, 0

        if week_totals:
            week_sum = week_totals.aggregate(total=models.Sum(amountType))['total']
        if month_totals:
            month_sum = (month_totals.aggregate(total=models.Sum(amountType))['total'] 
                         * 12 
                         / 365 
                         * 7)
        if year_totals:
            year_sum = (year_totals.aggregate(total=models.Sum(amountType))['total'] 
                        / 365 
                        * 7)
        return {(field+amount) : round((week_sum 
                                        + month_sum 
                                        + year_sum),
                                        2)}

    def get_discretionary(self, field:str, ruser):
        rateType = field + "_rate"
        amountType = field + "_amount"
        categoryType = field + "_category"

        discretionary_week = self.get_queryset().filter(user=ruser,
                                                        **{rateType: "Weekly"},
                                                        **{categoryType: "Discretionary"})
        discretionary_month = self.get_queryset().filter(user=ruser,
                                                        **{rateType: "Monthly"},
                                                        **{categoryType: "Discretionary"})
        discretionary_year = self.get_queryset().filter(user=ruser,
                                                        **{rateType: "Annually"},
                                                        **{categoryType: "Discretionary"})
        discretionary_week_total, discretionary_month_total, discretionary_year_total = 0, 0, 0
        if discretionary_week:
            discretionary_week_total = discretionary_week.aggregate(total=models.Sum(amountType))['total']
        if discretionary_month:
            discretionary_month_total = discretionary_month.aggregate(total=models.Sum(amountType))['total'] * 12 / 365 * 7
        if discretionary_year:
            discretionary_year_total = discretionary_year.aggregate(total=models.Sum(amountType))['total'] / 365 * 7

        return {field + "_discretionary_total" : round(discretionary_week_total 
                                                       + discretionary_month_total 
                                                       + discretionary_year_total, 
                                                       2)}
    
    def get_essential(self, field:str, ruser):
        rateType = field + "_rate"
        amountType = field + "_amount"
        categoryType = field + "_category"

        essential_week = self.get_queryset().filter(user=ruser, 
                                                    **{rateType: "Weekly"}, 
                                                    **{categoryType : "Essential"} )
        essential_month = self.get_queryset().filter(user=ruser,
                                                     **{rateType: "Monthly"},
                                                     **{categoryType: "Essential"})
        essential_year = self.get_queryset().filter(user=ruser,
                                                    **{rateType: "Annually"},
                                                    **{categoryType: "Essential"})
        
        essential_week_total, essential_month_total, essential_year_total = 0, 0, 0
        if essential_week:
            essential_week_total = essential_week.aggregate(total=models.Sum(amountType))['total']
        if essential_month:
            essential_month_total = essential_month.aggregate(total=models.Sum(amountType))['total'] * 12 / 365 * 7
        if essential_year:
            essential_year_total = essential_year.aggregate(total=models.Sum(amountType))['total'] / 365 * 7

        return {(field + "_essential_total") : round(essential_week_total 
                                                     + essential_month_total 
                                                     + essential_year_total, 
                                                     2)}